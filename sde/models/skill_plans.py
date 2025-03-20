from django.db import models


class SkillPlan(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    internal_name = models.TextField()
    milestones = models.JSONField(default=list)
    description = models.TextField()
    career_path_id = models.IntegerField(null=True, default=None)
    skill_requirements = models.JSONField(default=list)
    faction_id = models.IntegerField(null=True, default=None)

    def __str__(self):
        return f"{self.name}"
