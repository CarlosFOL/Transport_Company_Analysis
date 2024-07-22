import googlemaps
from group_manager import GroupManager, Point
from math import ceil, floor
import os
import pandas as pd



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
        self.client = googlemaps.Client(token)
        self.group_manager = GroupManager()
    

    def build_dist_table(self) -> pd.DataFrame:
        """
        It builds the distance table from the group of points created by the 
        GroupManager.
        """
        partition = [] 
        groups = self._create_groups()
        for g in groups:
            subset = self._design_subset(origins=g["ORIGEN"], destinations=g["DESTINO"])
            partition.append(subset)
        # We only have get the records that have a registered budget.
        dist_table = pd.merge(
            left = self.route_table,
            right = pd.concat(partition),
            on = ["ORIGEN", "DESTINO"],
            how="left"
        ).to_csv("../../data/budget_table.csv")
        return dist_table
    

    def _create_groups(self) -> list:
        """
        It creates the different groups of origin and destination points that 
        serve as inputs for the Google API. 
        
        Return
        ------
        list:
            Groups of origin and destination points.
        """
        # The manager starts with 0 groups. Therefore, we have to add the first one.
        self.group_manager.add_group() 
        # Go through each record of the route table
        ptypes = ['ORIGEN', 'DESTINO'] # Types of point
        for idx in range(self.route_table.shape[0]):
            origin, destination = [Point(name, ptype) 
                                   for name, ptype in zip(self.route_table.loc[idx, ptypes], ptypes)]
            # The second condition is to avoid strange cases.
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
                        break
                # If the destination point coult not be added to any group:
                if not destination.has_group:
                    self.group_manager.add_group(origin, destination)  
        return self.group_manager.show_groups()                       
    

    def _design_subset(self, origins: list, destinations: list) -> pd.DataFrame:
        """
        It gets the distance of a subset of a certain group of origin and destinations 
        points. And for this task, it calculates how many origin points can be sent
        in the request to avoid raising an error for exceeding the maximum number of
        elements.
        
        Parameters
        ----------
        origins: list
            Origin points of the routes
        destinations: list
            Destination points of the routes
        
        Return
        ------
        pd.DataFrame
            A partition
        """
        subset = []
        MAX_ELEMENTS = 25
        if len(destinations) <= MAX_ELEMENTS:
            # The number of origin points that we can choose:
            or_pts = floor(MAX_ELEMENTS / len(destinations))
            if or_pts >= len(origins):
                subset = self._send_request(origins, destinations)
            else:
                for i in range( ceil(len(origins) / or_pts) ):
                    block = self._send_request(origins[i*or_pts: (i*or_pts) + or_pts], destinations)
                    subset +=  block       
        else:
            dest_pts = ceil(len(destinations) / MAX_ELEMENTS)
            for o in origins:
                for j in range(dest_pts):
                    block = self._send_request(o, destinations[j*dest_pts: (j*dest_pts) + dest_pts])
                    subset += block
        return pd.DataFrame(subset, columns = ["ORIGEN", "DESTINO", "KM"])
        

    def _send_request(self, origins: list | str, destinations: list | str) -> list:
        """
        It sends the request to the Google API distance matrix, but respecting
        the maximum number of elements allowed.
        """
        partition = []
        response = self.client.distance_matrix(origins, destinations)['rows']
        # If only 1 origin point has been sent
        origins = [origins] if type(origins) == str else origins 
        for i, o_point in enumerate(origins):
            for j, d_point in enumerate(destinations):
                data = response[i]["elements"][j]
                if data['status'] == "OK":                                     
                    distance = round(data["distance"]["value"] / 1000, 2)
                    partition.append((o_point, d_point, distance))
        return partition.iloc[:, 2:]



def run():
    route_table = pd.read_csv('budgets.csv')
    token = os.getenv("GCP_DIST_MATRIX")
    DistanceCalculator(route_table, token).build_dist_table()



if __name__ == '__main__':
    run()