import random
from mesa import Agent

class Cell(Agent):
    '''Description of the grid points of the CA'''

    # Definitions of state variables    
    Susceptible = 1
    Infected = 2
    Recovered = 3
    
    def __init__(self,pos,model,init_state=0):
        '''Create cell in given x,y position, with given initial state'''
        super().__init__(pos,model)
        self.x,self.y = pos
        self.state = init_state
        self.timecounterI = 0
        self.inf = 0
        self.infduration = 5
        self._nextstate = None
        self._nextinf = None
        self._nextinfduration = None
        self.immduration = 5
        self.timecounterR = 0
        self._nextimmduration = 0

    def step(self):
        '''Compute the next state of a cell'''
        # Assume cell is unchanged, unless something happens below
        self._nextinf = self.inf
        self._nextinfduration = self.infduration
        self._nextstate = self.state
        self._nextimmduration = self.immduration
        

        # Susceptibles - might die or get infected
        if self.state == self.Susceptible:
            # Infection?
            neis = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False)
            tot_inf = 0.0
            for nei in neis:
                if nei.state == self.Infected:
                    tot_inf += nei.inf
            infprob = 0.0
            if tot_inf > 0:
                infprob = tot_inf / (tot_inf + self.model.h_inf)
            if random.random() < infprob:
                self._nextstate = self.Infected
                # Inherit infectivity of one infecting neighbour
                infprobsum = 0.0
                rand = random.uniform(0, tot_inf)
                self._nextinfduration = self.infduration
                for nei in neis:
                    if nei.state == self.Infected:
                        infprobsum += nei.inf
                        if rand < infprobsum:
                            # Inherit pathogen characteristics from infecting neighbour
                            self._nextinf = nei.inf


        # Infected - might die naturally or die after disease_duration
        elif self.state == self.Infected:
            if random.random() > 0.9:
                self.mutate_inherited_duration()
            if self.timecounterI > self.infduration:
               self._nextstate = self.Recovered
               self._nextimmduration = random.randint(1, self.immduration)
            else:
                ### CHANGED self.timecounter to self.timecounterI because self.timecounter is not defined
                self.timecounterI += 1
            
        elif self.state == self.Recovered:
            #print("print the immduration of this cell is", self.immduration)
            if self.timecounterR > self.immduration:
                self._nextstate = self.Susceptible
            else:
                self.timecounterR += 1
                
    def mutate_inherited_duration(self):
        delta_duration = random.randint(-10, 10)
        new_infection_duration = max(0,  self.infduration + delta_duration)
        self._nextinfduration = new_infection_duration

    def advance(self): 
        self.state = self._nextstate
        self.inf = self._nextinf
        self.infduration = self._nextinfduration
        self.immduration = self._nextimmduration

