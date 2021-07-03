class InsertData():

    D = {
        'title': None,
        'region': None,
        'mountain': None,
        'route_type': None,
        'altitude': None,
        'elevation_gain': None,
        'difficulty': None,
        'equipment': None,
        'shelter': None,
        'link': None,
        'note': None
    }

    def update(self,
               title=None, region=None, mountain=None, route_type=None, difficulty=None, altitude=None,
               elevation_gain=None, equipment=None, shelter=None, link=None, note=None):

        if title != '' and title is not None:
            self.D['title'] = title

        if region != '' and region is not None:
            self.D['region'] = region

        if mountain != '' and mountain is not None:
            self.D['mountain'] = mountain

        if route_type != '' and route_type is not None:
            self.D['route_type'] = route_type
        
        if difficulty != '' and difficulty is not None:
            self.D['difficulty'] = difficulty

        if altitude != '' and altitude is not None:
            self.D['altitude'] = altitude

        if elevation_gain != '' and elevation_gain is not None:
            self.D['elevation_gain'] = elevation_gain

        if equipment != '' and equipment is not None:
            self.D['equipment'] = equipment
        
        if shelter != '' and shelter is not None:
            self.D['shelter'] = shelter
        
        if link != '' and link is not None:
            self.D['link'] = link
        
        if note != '' and note is not None:
            self.D['note'] = note