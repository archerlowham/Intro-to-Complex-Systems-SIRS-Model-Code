from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from model import SIModel

''' Portrayal function: defines the portrayal of the cells '''
def portrayCell(cell):
    assert cell is not None
    portrayal = {"Shape": "rect",
                 "w": 1,
                 "h": 1,
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "white"} # Default colour, used for empty cells.
    if cell.state == cell.Susceptible:
        portrayal["Color"] = "grey"
    elif cell.state == cell.Infected:
        portrayal["Color"] = "red"
    elif cell.state == cell.Recovered:
        portrayal["Color"] = "green"

    return portrayal


''' Construct the simulation grid, all cells displayed as 5x5 squares '''
gridwidth = 100 # Change these parameters to change the grid size
gridheight = 100

# Make a grid to plot the population dynamics
grid = CanvasGrid(portrayCell, gridwidth, gridheight, 5*gridwidth, 5*gridheight)
# Make a chart for plotting the density of individuals
chart1 = ChartModule([{"Label": "S", "Color": "grey"},{"Label": "I", "Color": "red"}, {"Label": "R","Color": "green"}], data_collector_name='datacollector1')
# Let chart plot the mean infection time
chart2 = ChartModule([{"Label": "Mean_infduration", "Color": "Red"}, {"Label": "Mean_immduration", "Color": "Green"}, {"Label": "Mean_infectivity", "Color": "Yellow"}], data_collector_name='datacollector2')


''' Launch the server that will run and display the model '''
server = ModularServer(SIModel,
                       [grid, chart1, chart2],
                       "SI-model",
                       {"width": gridwidth, "height": gridheight})

