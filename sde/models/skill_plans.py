from django.db import models


class SkillPlan(models.Model):
    id = models.IntegerField(primary_key=True)
    career_path_id = models.IntegerField(null=True, default=None)
    faction_id = models.IntegerField(null=True, default=None)
    name = models.TextField()
    internal_name = models.TextField()
    milestones = models.JSONField(default=list)
    description = models.TextField()
    skill_requirements = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name}"
