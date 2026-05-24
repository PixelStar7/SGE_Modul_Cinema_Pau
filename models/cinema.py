# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 
from odoo.exceptions import ValidationError 


class Person(models.Model):
    _name = 'cinema.person'
    _description = 'Person Management'
    _order = 'full_name, birth_date desc'

    first_name = fields.Char("First Name", size=25, required=True)
    last_name = fields.Char("Last Name", size=45, required=True)

    # El deixo a name per a que sigui el nom que agafi Odoo per als registres
    name = fields.Char("Full Name", compute="_compute_full_name") 

    isDirector = fields.Boolean("Is Director", required=True)
    isActor = fields.Boolean("Is Actor", required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", required=True)

    birth_date = fields.Date("Birth Date", required=True)
    death_date = fields.Date("Death Date") # Opcional

    country_id = fields.Many2one('res.country', string="Citizenship", required=True, readonly=True)
    film_ids = fields.Many2many('cinema.film', string="Films", readonly=True)
    director_id = fields.Many2one('cinema.person', string="Directing Person", required=True, readonly=True)

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = record.last_name +  ", " + record.first_name

    # Quan es crea una Persona...
    @api.model_create_multi
    def create(self, values):
        # Mirem els nous valors i comparem si ja n'hi ha algun
        return

class Film(models.Model):
    _name = 'cinema.film'
    _description = 'Film Management'
    _order = 'title, year desc'
    _rec_name = 'title' # Aqui poso title al _rec_name

    title = fields.Char("Title", size=60, required=True, translate=True)
    year = fields.Integer("Release Year", required=True)

    # Duration in minutes with tooltip
    duration = fields.Integer("Duration", help="Duration in minutes", required=True)

    film_type = fields.Char("Film Type", compute="_compute_film_type", required=True)
    synopsis = fields.Text("Synopsis", translate=True) # Opcional
    website = fields.Char("Website", size=60) # Opcional

    poster = fields.Image("Poster") # Opcional

    director_id = fields.Many2one('cinema.person', string="Director", readonly=True)
    actor_ids = fields.Many2many('cinema.person', string="Actors", readonly=True)

    @api.depends('duration')
    def _compute_film_type(self):
        for record in self:
            if record.duration < 30:
                record.film_type = "Curtmetratge"
            elif record.duration > 30 and record.duration < 60:
                record.film_type = "Migmetratge"
            else:
                record.film_type = "Llargmetratge"

    @api.depends('year')
    def _check_year(self):
        for record in self:
            if record.year and record.year < 1895:
                raise ValidationError (_('There was no films before 1895!'))

    # Quan es crea un Film...
    @api.model_create_multi
    def create(self, values):
        # values és una llista de diccionaris. Cada diccionari és un film nou.
        for d in values:
            # Comprovem si s'està enviant el camp 'website' i si té algun valor
            if 'website' in d and d['website'] != False:
                d['sebsite'] = d['website'].lower() # Ho posem a minúscules
        
        films = super().create(values)

        return films
    
    # Quan es modifica un Film...
    def write(self, values):
        # self conté els registres a modificar
        # En el write, 'values' és un unic diccionari amb els camps que S'HAN MODIFICAT
        if 'website' in values and values['website'] != False:
            values['sebsite'] = values['website'].lower() # Ho posem a minúscules

        films = super().write(values)

        return films
