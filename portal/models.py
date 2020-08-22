from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.


# TODO update this department list
DEPARTMENTS = (
            ('ISE', 'Information Science Engineering'),
            ('CSE', 'Computer Science Engineering'),
            ('MECH', 'Mechanical'),
            ('ECE', 'Electronics and Communication Engineering'),
            ('CHEM', 'Chemical Engineering'),
            ('EEE', 'Electrical and Electronics Engineering'),
            ('CV', 'Civil Engineering'),
            ('TCE', 'Telecommunication Enginnering')
            )

class Student (models.Model):
    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other")
    )


    name = models.CharField(max_length=50 )
    USN = models.CharField(max_length=15, unique=True)
    CGPA = models.FloatField()
    department = models.CharField(max_length=5, choices=DEPARTMENTS)
    gender = models.CharField(choices=GENDER, max_length=5)
    eligiblility = models.BooleanField(default=True)
    website = models.URLField(blank=True)
    linkedin =  models.URLField(blank=True)
    is_placed = models.BooleanField(default=False)

    def __str__(self):
        return self.USN + " : " + self.name
    
    def get_absolute_url(self):
        return "/students/"+str(self.id)+"/" 


class Offer (models.Model):

    company_name = models.CharField(max_length=50)
    package = models.CharField(max_length=50, default="0")
    cutoff = models.FloatField(default=0)
    departments = MultiSelectField(choices=DEPARTMENTS)
    position = models.CharField(max_length=100, default="")
    link = models.URLField(blank=True)
    no_of_stages = models.IntegerField(blank=True, null=True)
    test_date = models.DateTimeField(blank=True, null=True)
    eligibility = models.TextField(blank=True)
    note = models.TextField(blank=True, default="")
    open_dream = models.BooleanField(default=False)


    def __str__(self):
        return self.company_name +" : "+ self.position

    def get_absolute_url(self):
        return "/offers/"+str(self.id)+"/"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs) 
    #     offer = Offer.objects.get(id = self.id)
    #     applications = Application.objects.filter(offer=offer )
    #     for application in applications:
            
    #         application.is_active = False
    #         application.save()
                



class Application(models.Model):

    STATUS = (
        ('PROCESS', "Application under process"),
        ('SELECTED', "Application Selected"),
        ('REJECTED', "Application Rejected"),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='applications')
    completed_stages = models.IntegerField(default=0)
    status = models.CharField(max_length=10,  choices=STATUS, default='PROCESS')
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = (('student', 'offer'),)

    def __str__(self):
        return self.student.USN +" - "+ self.offer.company_name

    def get_absolute_url(self):
        return "/applications/"+str(self.id)+"/"

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)  # Call the "real" save() method.

        print("________________________________ calling on save for Application")
        if self.status == 'SELECTED' and self.offer.open_dream == True:
    
            print("________________________________ selected in open dream company")

            student = Student.objects.get(id = self.student.id)
            student.eligiblility = False
            student.is_placed = True
            student.save()
            print("________________________________ student not eligible to apply further")

            applications = Application.objects.filter(student=student )
            for application in applications:
                if application.id != self.id:
                    print("________________________________ updating application status to inactive")
                    application.is_active = False
                    application.save()
                    