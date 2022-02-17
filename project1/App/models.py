from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
def is_esprit_mail(value):
    if not str(value).endswith('@esprit.tn'):
        raise ValidationError("Votre email est invalide",params={'value':value}) #ctrl double espace pour importer
# Create your models here.
#toutes les classes heritent de model.Models
class User(models.Model):
    nom=models.CharField(max_length=30)
    prenom=models.CharField(max_length=30)
    email=models.EmailField('Email',validators=[is_esprit_mail]) #esmou fel base Email
    def __str__(self):
        #return 'le prenom '+self.prenom+' le nom '+self.nom
        return f'le prenom {self.prenom} le nom {self.nom}'

class Etudiant(User): #herite de User
    groupe=models.CharField(max_length=30)
#
class Coach(User):
    pass #pas d'attributs à ajouter

class Projet(models.Model):
    nom_projet=models.CharField('Titre Projet',max_length=30)
    duree_projet=models.IntegerField('Duree Estimee',default=0)
    temps_alloue_par_projet=models.IntegerField('Temps alloue', validators=[MinValueValidator(1), MaxValueValidator(10)])
    besoin=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    est_valide=models.BooleanField(default=False)
    createur=models.OneToOneField(
        Etudiant,
        related_name='project_owner',
        on_delete=models.CASCADE
    )
    superviseur=models.ForeignKey(
        Coach,
        on_delete=models.SET_NULL,
        null=True,
        related_name='project_coach'
    )
    #through nom de la classe associer
    # relatedname nom de l association
    # on ajoute through si on a d'autre parametre
    members=models.ManyToManyField(
        Etudiant,
        through='MemberShipInProject',
        related_name='les_membres'
    )

class MemberShipInProject(models.Model):
    projet=models.ForeignKey(Projet,on_delete=models.CASCADE)
    etudiant=models.ForeignKey(Etudiant,on_delete=models.CASCADE)
    time_allocated_by_member=models.IntegerField('Temps alloue par membre')