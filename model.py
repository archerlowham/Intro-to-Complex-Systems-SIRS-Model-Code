import random

from mesa import Model
from mesa.time import SimultaneousActivation # updating scheme for synchronous updating
#from mesa.time import RandomActivation # for asynchronous updating
from mesa.space import SingleGrid # spatial grid
from mesa.datacollection import DataCollector # Data collection, to plot mean infectivity

from cell import Cell # Function that describes behaviour of single cells

# Computes the mean infection duration in all infected individuals
def compute_mean_infduration(model):
    infs = [cell.infduration for cell in model.schedule.agents if cell.state == cell.Infected]
    if len(infs) != 0:
        return sum(infs)/len(infs)
    else:
        return None

def compute_mean_immduration(model):
    recs = [cell.immduration for cell in model.schedule.agents if cell.state == cell.Recovered]
    if len(recs) != 0:
        return sum(recs)/len(recs)
    else:
        return None

def compute_mean_infectivity(model):
    infectivities = [cell.inf for cell in model.schedule.agents if cell.state == cell.Infected]
    if len(infectivities) != 0:
        return sum(infectivities)/len(infectivities)
    else:
        return None

# Computes the fraction of cells filled with an S individual
def fracS(model):
    nS = len([cell.state for cell in model.schedule.agents if cell.state == cell.Susceptible])
    return nS / len(model.schedule.agents)

# Computes the fraction of cells filled with an I individual
def fracI(model):
    nI = len([cell.state for cell in model.schedule.agents if cell.state == cell.Infected])
    return nI / len(model.schedule.agents)

def fracR(model):
    nR = len([cell.state for cell in model.schedule.agents if cell.state == cell.Recovered])
    return nR / len(model.schedule.agents)

class SIModel(Model):
    '''Description of the model'''
    
    def __init__(self, width, height):

        ### CHANGED: added super().__init__() to initialize the Model class
        super().__init__()
        
        # Set the model parameters
        self.infectivity = 5      # Infection strength per infected individual
        self.infection_duration = 5 # Duration of infection
        self.r = 0.04               # Reproduction rate per susceptible
        self.d = 0.05               # Natural death rate
        self.h_inf = 10            # Scaling of infectivity
        self.immunity_duration = 10
       
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = SimultaneousActivation(self)
        for (content,(x, y)) in self.grid.coord_iter():
            # Place randomly generated individuals
            cell = Cell((x,y), self)
            rand = random.random()
            if rand < 0.95:
                cell.state = cell.Susceptible
            elif rand < 1:
                cell.state = cell.Infected
                cell.inf = self.infectivity
                cell.infduration = random.randint(0, self.infection_duration)
                cell.timecounterI = random.randint(0, self.infection_duration)
            else:
                cell.state = cell.Recovered
                cell.immduration = random.randint(0, self.immunity_duration)
                cell.timecounterR = random.randint(0, self.immunity_duration)
            self.grid.place_agent(cell, (x,y))
            self.schedule.add(cell)

        # Add data collector, to plot the number of individuals of different types
        self.datacollector1 = DataCollector(model_reporters={"S": fracS, "I": fracI, "R": fracR})

        # Add data collector, to plot the mean infection duration
        self.datacollector2 = DataCollector(model_reporters={"Mean_infduration": compute_mean_infduration, "Mean_immduration": compute_mean_immduration, "Mean_infectivity": compute_mean_infectivity})

        self.running = True

    def step(self):
        self.datacollector1.collect(self)
        self.datacollector2.collect(self)
        self.schedule.step()

