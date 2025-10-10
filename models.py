from django.db import models
from django.contrib.auth.models import User
from utils import encrypt_data, decrypt_data
from cryptography.fernet import Fernet
from VotingSystem import settings



cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())

# Create your models here.


class Candidate(models.Model):
    candidate_name = models.CharField(max_length=100)
    candidate_party = models.CharField(max_length=100)
    candidate_symbol = models.ImageField(upload_to='symbols/')
    candidate_district = models.CharField(max_length=100)
    candidate_bio = models.TextField()


class Vote(models.Model):
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter_id = models.ForeignKey(User, on_delete=models.CASCADE)


class State(models.Model):
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.state


class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.district} ({self.state})"


class Municipality(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    municipality = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.municipality} ({self.district})"





class VoterDetails(models.Model):
    v_aadhaar = models.TextField(unique=True)
    v_id = models.TextField(unique=True)
    v_name = models.TextField()

    def save(self, *args, **kwargs):
        """Ensure encryption happens only once before saving to DB."""
        if not self.v_aadhaar.startswith("gAAAAA"):  # Check if already encrypted
            self.v_aadhaar = encrypt_data(self.v_aadhaar)
        if not self.v_id.startswith("gAAAAA"):
            self.v_id = encrypt_data(self.v_id)
        if not self.v_name.startswith("gAAAAA"):
            self.v_name = encrypt_data(self.v_name)
        super().save(*args, **kwargs)


    def get_decrypted_data(self):
        """Decrypt data when retrieving."""
        return {
            "v_aadhaar": decrypt_data(self.v_aadhaar),
            "v_id": decrypt_data(self.v_id),
            "v_name": decrypt_data(self.v_name),
        }
