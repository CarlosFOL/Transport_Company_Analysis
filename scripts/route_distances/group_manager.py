class Point:
    """
    It represents an origin or destination point in a particular route.
    
    Attributes
    ----------
    name: str
        Name of the origin or destination place.
    ptype: str
        Point type: 'origen' or 'destino' 
    """

    def __init__(self, name: str, ptype: str):
        self._name = name
        self._ptype = ptype
        self.has_group = False
        
    @property
    def name(self):
        return self._name
    
    @property
    def ptype(self):
        return self._ptype



class TripGroup:
    """
    Particular group of origin and destination points. 
    """
    
    def __init__(self):
        self.group_points = {"ORIGEN": [], "DESTINO": []}
    
    @property
    def content(self):
        """
        It returns the list of origin an destination points of the group.
        """
        return self.group_points
    
    def does_it_belong(self, point: Point) -> bool:
        """
        It checks if the sent point is in either the 'ORIGEN' or 'DESTINO' list
        according to its ptype.
        """
        return point.name in self.group_points[point.ptype] 
    
    def can_be_inserted(self, point: Point) -> bool:
        """
        It makes sure that the point is not in the list of its opposite ptype to 
        allow its insertion.
        """
        if point.ptype == "ORIGEN":
            opp_group = "DESTINO"
        else:
            opp_group = "ORIGEN"
        return point.name not in self.group_points[opp_group]
        
    def add_point(self, point: Point):
        """
        Add the point in the list corresponding to its ptype.
        """
        self.group_points[point.ptype].append(point.name)
        point.has_group = True
        


class GroupManager:
    """
    It manages the groups of origin and destination points. It ensures that in 
    a same group there won't be a same point in both origin or destination list.
    
    Attributes
    ----------
    groups: list
        It contains the different group of origin and destination points.
    """
    
    def __init__(self):
        self.groups = []
    
    def is_new(self, point: Point) -> bool:
        """
        It verifies if the point already exists in any trip group. 
        """
        for g in self.groups:
            if g.does_it_belong(point):
                return False
        return True
    
    def add_group(self, origin: Point = None, destination: Point = None) -> None:
        """
        It adds a new empty group or with a pair of points.
        """
        self.groups.append(TripGroup())
        if origin != None and destination != None:
            last_added = self.groups[-1]
            last_added.add_point(origin)
            last_added.add_point(destination)
    
    def which_group(self, new_point: Point) -> TripGroup:
        """
        It returns the group which the new point can be inserted. And If the 
        origin point cannot be inserted in any group, a new one is created
        """
        for n, g in enumerate(self.groups):
            if g.can_be_inserted(new_point):
                return self.groups[n]
        # If the new point is in the opposite list of each group:
        self.add_group()
        return self.groups[-1]
    
    def get_groups(self, point: Point) -> TripGroup:
        """
        It gets the group(s) where the origin point was added according to its ptype.
        """
        its_groups = []
        for g in self.groups:
            if g.does_it_belong(point):
                its_groups.append(g)
        return its_groups
        
    
    def show_groups(self) -> list:
        """
        It returns the groups of origin and destination points that the manager
        creates.
        """
        groups = []
        for g in self.groups:
            groups.append(g.content)
        return groups