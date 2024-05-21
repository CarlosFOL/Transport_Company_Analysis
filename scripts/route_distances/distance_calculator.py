import googlemaps
import pandas as pd
from group_manager import GroupManager, Point
from time import sleep

class DistanceCalculator:
    """
    Measure the distance in kilometers through a list of origin and destination
    points using Google Matrix Distance API.
    
    Attributes
    ----------
    route_table: pd.DataFrame
        It contains the route of the trips made by the transport company.
    token: str
        To authentificate in the Google Matrix Distance API.
    group_manager: GroupManger
        It's the responsible to add the origin and destination points to the 
        appropiate group.
    """
    
    def __init__(self, route_table: pd.DataFrame, token = str):
        self.route_table = route_table
        self.token = token
        self.group_manager = GroupManager()
    
    def _create_groups(self) -> list:
        """
        It creates the two groups of origin and destination points that serve as
        inputs for the Google API. 
        
        Return
        ------
        list:
            Groups of origin and destination points.
        """
        # The manager starts with 0 groups. Therefore, we have to add the first one.
        self.group_manager.add_group() 
        # Go through each record of the route table
        ptypes = ['ORIGEN', 'DESTINO']
        for idx in range(self.route_table.shape[0]):
            origin, destination = [Point(name, ptype) 
                                   for name, ptype in zip(self.route_table.loc[idx, ptypes], ptypes)]
            # The second condition is to avoid stange cases.
            if self.group_manager.is_new(origin) and (origin.name != destination.name):
                # In which group can the new point be inserted?
                group = self.group_manager.which_group(origin)
                # If the destination is already in the group.
                if group.does_it_belong(destination):
                    group.add_point(origin)
                # If the destination point does not belong to the group and it can be inserted
                elif not group.does_it_belong(destination) and group.can_be_inserted(destination):
                    group.add_point(origin)
                    group.add_point(destination)
                else:
                    # When the origin point can be added to an existing group, but the destiantion cannot.
                    self.group_manager.add_group(origin, destination)
            elif not self.group_manager.is_new(origin) and (origin.name != destination.name):
                # Verify in which groups the origin point was added:
                groups = self.group_manager.get_groups(origin)
                # Check in which one the destination point can be inserted              
                for g in groups:
                    if g.does_it_belong(destination):
                        destination.has_group = True
                        break
                    elif not g.does_it_belong(destination) and g.can_be_inserted(destination):
                        g.add_point(destination)
                        destination.has_group = True
                        break
                # If the destination point cannot be added to any group:
                if not destination.has_group:
                    self.group_manager.add_group(origin, destination)  
        return self.group_manager.show_groups()                       
    
    def build_dist_table(self):
        """
        It builds the distance table from the group of points created by the 
        GroupManager.
        """
        client = googlemaps.Client(key = self.token)
        groups = self._create_groups()
        for g in groups:
            distances = 0
        
        

def run():
    route_table = pd.read_csv('budget_table.csv')
    with open('api_key.txt', 'r') as f:
        token = f.read()
    dist_cal = DistanceCalculator(route_table, token)
    groups = dist_cal._create_groups()
    for g in groups:
        print(g)



if __name__ == '__main__':
    run()
    # client = googlemaps.Client(key = 'AIzaSyAJjt79ls7XqGM_Cx4MpAMcpQLjptkdmrk')
    # origin = ['New York, USA', 'Boston, USA']
    # destination = ['Orlando, Florida, USA', 'Miami, USA']
    # response = client.distance_matrix(origin, destination)
    # with open('response.txt', 'w', encoding='utf-8') as f:
    #     f.write(f'{response}')



