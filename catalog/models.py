from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from schedule.models import Calendar, Event


class Person(models.Model):
  name = models.CharField(max_length=255)
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person', null=True, blank=True)
  parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

  class Preference(models.IntegerChoices):
        ANYONE = 1, 'Anyone can stay here'
        KNOWN_PEOPLE = 2, 'Only people well known to TO can stay here'
        MEMBERS = 3, 'Only TO members can stay here'

  preference = models.IntegerField(
        choices=Preference.choices,
        default=Preference.ANYONE,
        
    )
  
  def __str__(self):
    return self.name

# Create your models here.
class Building(models.Model):
  name = models.CharField(max_length = 255)
  is_offline = models.BooleanField(default=False)
  area = models.CharField(max_length = 255)
  
  def __str__(self):
    return self.name
  
class Section(models.Model):
  building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='sections')
  name = models.CharField(max_length=255)
  is_offline = models.BooleanField(default=False)
  image = models.ImageField(upload_to='room_images/', null=True, blank=True)

  def __str__(self):
    return f"{self.building.name} / {self.name}"
  
  def save(self, *args, **kwargs):
        # Check if is_offline has changed
        if self.pk:  # This ensures we are updating an existing instance
            previous = Section.objects.get(pk=self.pk)
            if (previous.is_offline != self.is_offline) and self.is_offline:
              self.delete_availability_events()
                          
                  
                
        super().save(*args, **kwargs)  # Call the original save method
      

  def delete_availability_events(self):
      rooms = self.rooms.all()

      for room in rooms:
          calendar = room.calendar
          if calendar:
              CustomEvent.objects.filter( calendar=calendar).delete()

            
      


class Room(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='rooms')
    number = models.IntegerField()
    calendar = models.OneToOneField(Calendar, on_delete=models.SET_NULL, null=True, blank=True, related_name='room')
    owner = models.OneToOneField(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='room')
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)
    is_offline = models.BooleanField(default=False)
  
    def __str__(self):
        return f"{self.section.building.name} / {self.section.name} / {self.number}"

    def is_available(self, start_date, end_date):
        if not self.calendar:
            return True

        # Ensure dates are timezone aware
        if timezone.is_naive(start_date):
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        if timezone.is_naive(end_date):
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())
      
        occupancy_events_exist = CustomEvent.objects.filter(
            calendar=self.calendar,
            event_type='occupancy',
            start__lt=end_date,
            end__gt=start_date
        ).exists()

        if occupancy_events_exist:
            return False

        availability_events = CustomEvent.objects.filter(
            calendar=self.calendar,
            event_type='availability',
            start__lte=start_date,
            end__gte=end_date
        )

        # Check for available and not occupied
        return availability_events.exists() and not self.is_offline
  
    def get_last_available_date(self, start_date):
        if not self.calendar:
            return None

        if timezone.is_naive(start_date):
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())

        # Fetch current availability event
        current_availability = CustomEvent.objects.filter(
            calendar=self.calendar,
            event_type='availability',
            start__lte=start_date,
            end__gte=start_date
        ).first()

        if not current_availability:
            return None

        # Fetch next occupancy event within the availability window
        next_occupancy = CustomEvent.objects.filter(
            calendar=self.calendar,
            event_type='occupancy',
            start__gte=start_date,
            start__lt=current_availability.end
        ).order_by('start').first()

        if next_occupancy:
            return min(current_availability.end, next_occupancy.start)
        else:
            return current_availability.end

    def save(self, *args, **kwargs):
        old_owner = None

        if self.pk:  # If the room already exists
            old_owner = Room.objects.get(pk=self.pk).owner
        
        super().save(*args, **kwargs)

        # Ensure the room has a calendar
        if not self.calendar:
            self.calendar = Calendar.objects.create()
            print('Creating calendar because there isn\'t one (ROOM SAVE)')
            self.save(update_fields=['calendar'])

        # Update the calendar name
        if self.owner:
            self.calendar.name = f"{self.owner.name}'s Calendar"  # Customize as needed
            print('Naming calendar after owner (ROOM SAVE)')
        else:
            self.calendar.name = f"Room {self.number} in {self.section}"
            print("Naming calendar after room because no owner (ROOM SAVE)")

        self.calendar.save()

        # Create a specific datetime object far in the future
        never_date = datetime(2999, 12, 31, 12, 0, 0)  # December 31, 2999 at noon
        # Make it timezone-aware
        never_date = timezone.make_aware(never_date, timezone.get_current_timezone())

        if not self.owner:
            # Create or update a permanent availability event
            CustomEvent.objects.update_or_create(
                calendar=self.calendar,
                event_type='availability',
                defaults={
                    'start': timezone.now(),
                    'end': never_date,
                    'title': "Permanent Availability"
                }
            )
        else:
            if old_owner != self.owner:
                # Owner has changed, delete availability events
                CustomEvent.objects.filter(
                    calendar=self.calendar,
                    event_type='availability'
                ).delete()

        super().save(*args, **kwargs)
  







    
class CustomEvent(Event):
    EVENT_TYPES = (
        ('occupancy', 'Occupancy'),
        ('availability', 'Availability'),
    )

    class GuestType(models.IntegerChoices):
        STRANGER = 1, 'Stranger'
        KNOWN = 2, 'Known'
        MEMBER = 3, 'Member'

    guest_type = models.IntegerField(
        choices=GuestType.choices,
        default=GuestType.STRANGER,
        null=True, blank=True# Default to "Anyone can stay here"
    )
    guest_name = models.CharField(max_length=20, blank = True , null=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    
    def save(self, *args, **kwargs):
        print("Custom event is saving...")
        # Ensure start and end are timezone-aware
        if timezone.is_naive(self.start):
            self.start = timezone.make_aware(self.start, timezone.get_current_timezone())
        if timezone.is_naive(self.end):
            self.end = timezone.make_aware(self.end, timezone.get_current_timezone())
        print(f"Saving CustomEvent: {self.title}")
        super(CustomEvent, self).save(*args, **kwargs)
    

# Signal to delete Calendar when Room is deleted
@receiver(post_delete, sender=Room)
def delete_calendar_when_room_deleted(sender, instance, **kwargs):
    if instance.calendar:
        instance.calendar.delete()


@receiver(post_save, sender=Building)
def set_sections_and_rooms_offline(sender, instance, **kwargs):
    sections = instance.sections.all()
    for section in sections:
        if section.is_offline != instance.is_offline:
            section.is_offline = instance.is_offline
            section.save()

@receiver(post_save, sender=Section)
def set_rooms_offline(sender, instance, **kwargs):
    rooms = instance.rooms.all()
    for room in rooms:
        if room.is_offline != instance.is_offline:
            room.is_offline = instance.is_offline
            room.save()
