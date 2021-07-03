# This is the main Python script. Based on Python version 3.9.5

# Created by Riccardo Brusa on 30/06/2021.
# Copyright © 2021 Riccardo Brusa, Simone Accarino. All rights reserved.

import sys
import os
import yaml
import urllib.request

sys.path.append(os.path.abspath('..'))
from utils.database import DataBase
from utils.common import InsertData

from kivy.app import App
from kivy.base import runTouchApp
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ColorProperty
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, WipeTransition, FadeTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

app_path = os.path.dirname(__file__)
os.chdir(app_path)

with open(os.path.join(app_path, os.path.abspath('..'), 'config', 'config.yml'), 'r', encoding='utf-8') as ymlcfg:
    config = yaml.load(ymlcfg, Loader=yaml.FullLoader)['mountain-gui']
    prod = config['prod']
    enable_db = config['enable_db']
    # mysql parameters
    if prod:
        mysql_host = config['mysql']['prod']['host']
        mysql_db = config['mysql']['prod']['db']
        mysql_table = config['mysql']['prod']['table']
    else:
        mysql_host = config['mysql']['test']['host']
        mysql_db = config['mysql']['test']['db']
        mysql_table = config['mysql']['test']['table']
    # kivy parameters
    Screen.title_font_size = config['kivy']['font_size']['title']
    Screen.label_font_size = config['kivy']['font_size']['label']
    Screen.button_font_size = config['kivy']['font_size']['button']
    Screen.error_font_size = config['kivy']['font_size']['error']
    Screen.homepage = config['kivy']['images']['homepage']
    Screen.errorpage = config['kivy']['images']['error']


global db
global insert_data
insert_data = InsertData()


class Error(Screen):

    error_message = 'Errore'

    def set_error(self, err=None):
        if err is not None:
            self.ids.error_label.text = err

    def retry(self):
        self.manager.transition = WipeTransition()
        self.manager.current = 'login'
        self.manager.get_screen('login').reset()


class Search(Screen):
    pass


class Insert(Screen):

    insert_title = config['kivy']['text']['insert_title']

    def init(self):

        if self.get_step() == 1:
            insert_data = InsertData()
    
    def print(self):
        print('--- to insert dict ---')
        print('title: {}'.format(insert_data.D['title']))
        print('region: {}'.format(insert_data.D['region']))
        print('mountain: {}'.format(insert_data.D['mountain']))
        print('route_type: {}'.format(insert_data.D['route_type']))
        print('altitude: {}'.format(insert_data.D['altitude']))
        print('elevation_gain: {}'.format(insert_data.D['elevation_gain']))
        print('equipment: {}'.format(insert_data.D['equipment']))
        print('difficulty: {}'.format(insert_data.D['difficulty']))
        print('shelter: {}'.format(insert_data.D['shelter']))
        print('link: {}'.format(insert_data.D['link']))
        print('note: {}'.format(insert_data.D['note']))
    
    def get_step(self):

        return self.ids.display_step.step

    def set_step(self, step):

        self.ids.display_step.step = step
        self.ids.progress_bar.value = .333 * step

    def next(self,
             title=None, region=None, mountain=None, route_type=None, difficulty=None, altitude=None,
             elevation_gain=None, equipment=None, shelter=None, link=None, note=None):

        insert_data.update(title=title, region=region, mountain=mountain,
                           route_type=route_type, altitude=altitude, difficulty=difficulty,
                           elevation_gain=elevation_gain, equipment=equipment, shelter=shelter,
                           link=link, note=note)

        next_step = self.ids.display_step.step + 1
        next_name = 'insertstep{}'.format(next_step)

        self.manager.transition = WipeTransition()
        self.manager.current = next_name
        self.manager.get_screen(next_name).set_step(next_step)
        self.print()


class InsertStep1(Insert):
    
    def validate_data(self):

        alert = ''
        valid_data = True

        typed_title = self.ids.title.text.strip()
        typed_region = self.ids.region.text.strip()
        typed_mountain = self.ids.mountain.text.strip()
        typed_route_type = self.ids.route_type.text.strip()
        typed_altitude = self.ids.altitude.text.strip()

        if typed_title == '' or typed_title is None:
            print('[WARNING] Empty title')
            alert += ' - Campo <Titolo> obbligatorio'
            valid_data = False
        if typed_altitude != '' and typed_altitude is not None:
            if not typed_altitude.isnumeric():
                print('[WARNING] Altitude must be a number')
                alert += ' - <Altitudine> non valida'
                valid_data = False
        if 'clicca per selezionare' in typed_route_type.lower():
            typed_route_type = None

        if valid_data:
            self.next(title=typed_title, region=typed_region, mountain=typed_mountain,
                      route_type=typed_route_type, altitude=typed_altitude)
        else:
            self.ids.alert.alert = alert.strip(' - ')

        

class InsertStep2(Insert):
    
    def validate_data(self):

        alert = ''
        valid_data = True

        typed_elevation_gain = self.ids.elevation_gain.text.strip()
        typed_difficulty = self.ids.difficulty.text.strip()
        typed_equipment = self.ids.equipment.text.strip()
        typed_shelter = self.ids.shelter.text.strip()

        if typed_elevation_gain != '' and typed_elevation_gain is not None:
            if not typed_elevation_gain.isnumeric():
                print('[WARNING] <Elevation gain> must be a number')
                alert += ' - <Dislivello> non valido'
                valid_data = False
        
        if valid_data:
            self.next(elevation_gain=typed_elevation_gain, difficulty=typed_difficulty,
                      equipment=typed_equipment, shelter=typed_shelter)
        else:
            self.ids.alert.alert = alert.strip(' - ')
    

class InsertStep3(Insert):
    
    def validate_data(self):

        alert = ''
        valid_data = True

        typed_link = self.ids.link.text.strip()
        typed_note = self.ids.note.text.strip()

        if typed_link != '' and typed_link is not None:
            try:
                status_code = urllib.request.urlopen(typed_link).getcode()
                if status_code != 200:
                    print('[WARNING] <Link> is not reachable')
                    alert += ' - <Link> non raggiungibile'
                    valid_data = False
            except:
                print('[WARNING] <Link> is not reachable')
                alert += ' - <Link> non raggiungibile'
                valid_data = False
        
        if valid_data:
            self.next(link=typed_link, note=typed_note)
        else:
            self.ids.alert.alert = alert.strip(' - ')


class HomePage(Screen):

    home_title = config['kivy']['text']['home_title']
    
    def search(self):

        self.manager.transition = WipeTransition()
        self.manager.current = 'search'
        self.manager.get_screen('search')
    
    def insert(self):
        
        self.manager.transition = WipeTransition()
        self.manager.current = 'insertstep1'
        self.manager.get_screen('insertstep1')

class Login(Screen):

    main_title = config['kivy']['text']['main_title']

    def login(self):

        mysql_user = self.ids.user.text
        mysql_psw = self.ids.psw.text

        if enable_db:
            db = DataBase(mysql_db, mysql_user, mysql_psw, host=mysql_host)
            db_error = db.connection_error()
        else:
            db_error = None

        if db_error is None:
            self.manager.transition = WipeTransition()
            self.manager.current = 'homepage'
            self.manager.get_screen('homepage')
        else:
            print('[ERROR] Failed connection to {0} db'.format(db.db))
            self.manager.transition = WipeTransition()
            self.manager.current = 'error'
            self.manager.get_screen('error').set_error(config['kivy']['text']['error']['auth'])
    
    def reset(self):

        self.ids.user.text = ''
        self.ids.psw.text = ''
        

class MountainGUIApp(App):

    def build(self):

        manager = ScreenManager()
        manager.add_widget(Login(name='login'))
        manager.add_widget(Error(name='error'))
        manager.add_widget(HomePage(name='homepage'))
        manager.add_widget(Search(name='search'))
        manager.add_widget(InsertStep1(name='insertstep1'))
        manager.add_widget(InsertStep2(name='insertstep2'))
        manager.add_widget(InsertStep3(name='insertstep3'))

        return manager


if __name__ == '__main__':
    
    MountainGUIApp().run()