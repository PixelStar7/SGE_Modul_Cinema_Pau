# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 
from odoo.exceptions import ValidationError 


class CinemaPerson(models.Model):
    _name = 'cinema.person'
    _description = 'Person Management'
    _rec_name = 'full_name'
    _order = 'full_name, birth_date desc'

    first_name = fields.Char("First Name", size=25, required=True)
    last_name = fields.Char("Last Name", size=45, required=True)

    full_name = fields.Char("Full Name", compute="_compute_full_name") 

    isDirector = fields.Boolean("Is Director", required=True)
    isActor = fields.Boolean("Is Actor", required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", required=True)

    birth_date = fields.Date("Birth Date", required=True)
    death_date = fields.Date("Death Date") # Opcional

    country_id = fields.Many2one('res.country', string="Citizenship", required=True) # Les Many2One NO poden ser readonly=True

    film_directed_ids = fields.One2many('cinema.film', 'director_id', string="Directed Films", readonly=True)

    # Relació Many2many (Persons --> Films)
    # Nom de la taula que relacionarà / nom de la taula a crear / nom dels camps - de la nova taula / nom de la relació
    # El nom de la taula serà el mateix que en l'altre relació a "Film", amb les ids canviades d'ordre.
    film_acting_ids = fields.Many2many('cinema.person', 'cinema_person_film_rel', 'person_id', 'film_id', string="Acted Films", readonly=True)

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = record.last_name +  ", " + record.first_name

    # Quan es crea una Persona...
    @api.model_create_multi
    def create(self, values):
        # Mirem els nous valors i comparem si ja n'hi ha algun
        return

class CinemaFilm(models.Model):
    _name = 'cinema.film'
    _description = 'Film Management'
    _rec_name = 'title' # Aqui poso title al _rec_name
    _order = 'title, year desc'

    title = fields.Char("Title", size=60, required=True, translate=True)
    year = fields.Integer("Release Year", required=True)

    # Duration in minutes with tooltip
    duration = fields.Integer("Duration", help="Duration in minutes", required=True)

    # Per a que quedi enregistrat a la BD --> store=True
    film_type = fields.Char("Film Type", compute="_compute_film_type", store=True)

    synopsis = fields.Text("Synopsis", translate=True) # Opcional
    website = fields.Char("Website", size=60) # Opcional

    poster = fields.Binary("Poster") # Opcional

    director_id = fields.Many2one('cinema.person', string="Director", required=True)

    # Relació Many2many (Films --> Persons)
    # Nom de la taula que relacionarà / nom de la taula a crear / nom dels camps - de la nova taula / nom de la relació
    # El nom de la taula serà el mateix que en l'altre relació a "Person", amb les ids canviades d'ordre.
    actor_ids = fields.Many2many('cinema.person', 'cinema_person_film_rel', 'film_id', 'person_id', 'Actors', readonly=True)

    @api.depends('duration')
    def _compute_film_type(self):
        for record in self:
            if record.duration < 30:
                record.film_type = "Curtmetratge"
            elif record.duration > 30 and record.duration < 60:
                record.film_type = "Migmetratge"
            else:
                record.film_type = "Llargmetratge"

    # Per a checks, s'usa constrains
    @api.constrains('year')
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
                d['website'] = d['website'].lower() # Ho posem a minúscules
        
        films = super().create(values)

        return films
    
    # Quan es modifica un Film...
    def write(self, values):
        # self conté els registres a modificar
        # En el write, 'values' és un unic diccionari amb els camps que S'HAN MODIFICAT
        if 'website' in values and values['website'] != False:
            values['website'] = values['website'].lower() # Ho posem a minúscules

        films = super().write(values)

        return films

