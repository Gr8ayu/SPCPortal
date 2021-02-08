from django.db import models
from multiselectfield import MultiSelectField
import datetime
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
# TODO update this department list
DEPARTMENTS = (
            ('ISE', 'Information Science Engineering'),
            ('CSE', 'Computer Science Engineering'),
            ('MECH', 'Mechanical'),
            ('ECE', 'Electronics and Communication Engineering'),
            ('CHEM', 'Chemical Engineering'),
            ('EEE', 'Electrical and Electronics Engineering'),
            ('CV', 'Civil Engineering'),
            ('TCE', 'Telecommunication Enginnering'),
            ('PLAC','Placement Department')
            )

GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('OTHER', 'OTHER')

    )

USER_TYPE = (
        ('STUDENT', 'STUDENT'),
        ('TEACHER', 'TEACHER'),
        ('ADMIN', 'ADMIN')

    )

class User(AbstractUser):
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default="STUDENT")

    def is_student(self):
        return self.user_type == 'STUDENT'
    def is_teacher(self):
        return self.user_type == 'TEACHER'
    def is_admin_access(self):
        return self.user_type == 'ADMIN'

    def is_admin(self):
        return self.user_type == 'ADMIN'


class Department(models.Model):
    name = models.CharField(max_length=50 )
    # hod = models.ForeignKey(Faculties, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    group_email = models.EmailField()
    def __str__(self):
        return self.name

class Student(models.Model):

    user = models.OneToOneField(User, on_delete =models.CASCADE, related_name='student' )
    name = models.CharField(max_length=100)
    USN = models.CharField(max_length=20,  null=True)
    gender = models.CharField(max_length=10, choices=GENDER, blank=True )
    date_of_birth = models.DateField(default=datetime.datetime.today)
    profile_pic = models.ImageField(upload_to='profile_pic', default='profile_pic/default_pic.png') 
    resume = models.FileField(upload_to='resume', blank=True, null=True) 
    is_eligible = models.BooleanField(default=True)

    #  IS PLACED ?
    # TODO add more feilds later

    def __str__(self):
        return str(self.name) +" (" + self.user.email + ")"

    def is_placed(self):
        applications  = Application.objects.filter(student=self, status='ACCEPTED', offer__offer_type='OPEN')
        if applications.count() > 0:
            return applications
        else:
            return None

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    pass
    if created:
        Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if not instance.student:
        pass
        Student.objects.create(user=instance)
    instance.student.save()

@receiver(post_save, sender=Student)
def create_edu_contact(sender, instance, created, **kwargs):
    if created:
        pass
        Contact.objects.create(user=instance)
        Education.objects.create(user=instance)

@receiver(post_save, sender=Student)
def save_edu_contact(sender, instance, **kwargs):

    if not instance.contact:
        Contact.objects.create(user=instance)
    
    if not instance.education:
        Education.objects.create(user=instance)
    
    instance.contact.save()
    instance.education.save()



class Contact(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='contact')
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    pin = models.IntegerField( blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True)
    alternate_mobile = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True, null =True)

    def __str__(self):
        return str(self.user)

class  Education(models.Model):
    MODE  = (
            ("MGMT","Management"),
            ("KCET", "KCET" ),
            ("COMEDK", "COMEDK" )
        )
    user = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='education' )
    bio = models.TextField(blank=True)
    sem = models.IntegerField( default=1)

    admission_mode = models.CharField(max_length=10, choices=MODE, default='COMEDK')
    admission_mode_rank = models.IntegerField( null=True, blank=True)
    no_of_backlogs = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True )
    X_board = models.CharField(max_length=20, help_text="10th Board name", blank=True )
    XII_board = models.CharField(max_length=20, help_text="12th/Diploma Board name", blank=True  )
    X_percentage = models.FloatField( help_text="10th percentage", default=0 )
    XII_percentage = models.FloatField( help_text="12th percentage", default=0 )
    sem_1_sgpa = models.FloatField(null = True, blank = True, default = 0)
    sem_2_sgpa = models.FloatField(null = True, blank = True, default = 0)
    sem_3_sgpa = models.FloatField(null = True, blank = True, default = 0)
    sem_4_sgpa = models.FloatField(null = True, blank = True, default = 0)
    sem_5_sgpa = models.FloatField(null = True, blank = True, default = 0)
    sem_6_sgpa = models.FloatField(null = True, blank = True, default = 0)
    sem_7_sgpa = models.FloatField(null = True, blank = True, default = 0)
    sem_8_sgpa = models.FloatField(null = True, blank = True, default = 0)
    cgpa = models.FloatField(null = True, blank = True, default = 0)
    graduation_year = models.IntegerField(default = datetime.datetime.now().year)
    #TODO add backlog details, sem, bio, comedk rank


    def __str__(self):
        return str(self.user)

class Company(models.Model):
    COMPANY_CATEGORY = (
            ('Business Analytics','Business Analytics'),
            ('Communication and Engineering','Communication and Engineering'),
            ('Construction and Engineering','Construction and Engineering'),
            ('Consultancy','Consultancy'),
            ('Global Fianance Service','Global Fianance Service'),
            ('Health Care Division','Health Care Division'),
            ('R & D Division','R & D Division'),
            ('R & D Media and Mobile Applications','R & D Media and Mobile Applications'),
            ('Supply Chain Management','Supply Chain Management'),
            ('Production and Manufacturing','Production and Manufacturing'),
            ('Other','Other'),
        )


    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="company_logo",default='company_logo/default.png' )
    category = models.CharField(max_length=40, choices=COMPANY_CATEGORY, default='Other')
    
    def __str__(self):
        return self.name


class Offer(models.Model):
    OFFER_TYPE = (
            ('DREAM',"Dream"),
            ('OPEN',"Open Dream"),
        )

    CATEGORY = (
            ('INTERNSHIP',"Internship"),
            ('PLACEMENT',"Placement"),
        )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='offer')
    date = models.DateTimeField(default=datetime.datetime.now)
    deadline = models.DateTimeField()
    offer_type = models.CharField(max_length=20, default='DREAM', choices=OFFER_TYPE)
    category = models.CharField(max_length=20, default='INTERNSHIP', choices=CATEGORY)
    
    required_batch = models.IntegerField( null=True, blank=True)
    eligible_branches = models.ManyToManyField(Department, related_name="eligible_branches")
    eligible_gender = MultiSelectField(choices=GENDER, default='OTHER')
    package = models.FloatField(help_text="CTC in LPA", null=True, blank=True)
    note = models.TextField(blank=True)
    cgpa_cutoff = models.FloatField(default=0)
    X_cutoff = models.FloatField(default=0)
    XII_cutoff = models.FloatField(help_text="12th/Diploma cutoff percentage", default=0)
    max_backlog = models.IntegerField(default=0)
    bio_keyword = models.CharField(max_length=30, blank=True)
    # diploma_cutoff = models.FloatField(default=0)

    def __str__(self):
        return self.company.name

    def accepted(self):
        return Application.objects.filter(offer=self).filter(status="ACCEPTED").count()

class Application(models.Model):
    STATUS = (
        ('PROCESSING','PROCESSING'),
        ('ACCEPTED','ACCEPTED'),
        ('REJECTED','REJECTED'),
        ('HOLD','HOLD'),
        ('WITHDRAWN','WITHDRAWN'),
        ('OTHER','OTHER'),
        )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=10, choices=STATUS, default='PROCESSING')
    
    def __str__(self):
        return self.student.name

@receiver(post_save, sender=Application)
def save_edu_contact(sender, instance, **kwargs):

    if instance.status == 'ACCEPTED' and instance.offer.offer_type == 'OPEN':
        student = instance.student
        student.is_eligible = False
        student.save()
    # if not instance.contact:
    #     Contact.objects.create(user=instance)
    
    # if not instance.education:
    #     Education.objects.create(user=instance)
    
    # instance.contact.save()
    # instance.education.save()




class SPC(models.Model):
    students = models.ForeignKey(Student, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    def __str__(self):
        return self.students.name


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True )
    email = models.EmailField()
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class DepartmentGroupEmail(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    graduation_year = models.IntegerField()

    def __str__(self):
        return self.email