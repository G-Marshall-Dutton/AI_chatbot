from durable.lang import *

with ruleset('have_all_train_info'):
    @when_all(c.to << m.to != '',
              c.frm << m.frm != '')
    # the event pair will only be observed once
    def getTicket(c):
        print('Getting Ticket for journey...')
        print('%15s:%10s\n%15s:%10s'%('Leaving From',c.frm.frm,'Arriving At',c.to.to))
        

class ConversationController():
    def __init__(self):
        self.knowledge = {}
    
    def updateKnowldge(self,newKnowledge):
        for field in newKnowledge:
            self.knowledge.update(newKnowledge)
            print("ADDED -> ",newKnowledge)

            #Update ruleset with new data
            post('have_all_train_info', {field:newKnowledge.get(field)})



controller = ConversationController()
controller.updateKnowldge({'to':"norwich"})
controller.updateKnowldge({'frm':"bristol"})