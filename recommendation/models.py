from django.db import models

# This is an auto-generated Django model module.# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class League(models.Model):
    le_id = models.AutoField(primary_key=True)
    le_name = models.CharField(max_length=15)

    def __str__(self):
        return self.le_name

    class Meta:
        db_table = 'league'

class MatchSchedule(models.Model):
    ms_id = models.AutoField(primary_key=True)
    ms_league = models.ForeignKey(League, models.DO_NOTHING, db_column='ms_league')
    ms_team1 = models.ForeignKey('Team', models.DO_NOTHING, db_column='ms_team1', related_name='+')
    ms_team2 = models.ForeignKey('Team', models.DO_NOTHING, db_column='ms_team2', related_name='+')
    ms_time = models.DateTimeField(blank=True, null=True)
    ms_round = models.IntegerField()
    ms_season = models.IntegerField()
    ms_team1_score = models.IntegerField(blank=True, null=True)
    ms_team2_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} VS {}'.format(self.ms_team1, self.ms_team2)

    class Meta:
        db_table = 'match_schedule'

class Player(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=50)
    t = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True)
    active_flag = models.BooleanField(default=True)

    def __str__(self):
        return self.p_name

    class Meta:
        db_table = 'player'

class Round(models.Model):
    r_id = models.AutoField(primary_key=True)
    r_name = models.CharField(max_length=20)

    def __str__(self):
        return self.r_name

    class Meta:
        db_table = 'round'

class Team(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_name = models.CharField(max_length=50)
    t_shortname = models.CharField(max_length=50)
    t_code = models.CharField(max_length=50)

    def __str__(self):
        return self.t_name

    class Meta:
        db_table = 'team'

class UserWatch(models.Model):
    u_id = models.CharField(primary_key=True, max_length=32)
    ms = models.ForeignKey(MatchSchedule, models.DO_NOTHING)

    class Meta:
        db_table = 'user_watch'
        unique_together = (('u_id', 'ms'),)

class MatchProfileValues(models.Model):
    mv_id = models.AutoField(primary_key=True)
    ms_id = models.ForeignKey(MatchSchedule, models.DO_NOTHING)
    mv_cs = models.FloatField()

    class Meta:
        db_table = 'match_profile_values'

class UserWatchGenerateQueries(models.Model):
    # this id is the id that I'm using on interface i.e. u1, u2, u3
    uwg_id = models.CharField(max_length=3, primary_key=True)
    uwg_query = models.TextField(max_length=1000)
    uwg_description = models.TextField(blank=True)

    class Meta:
        db_table = 'user_watch_generate_queries'