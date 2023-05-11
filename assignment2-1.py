import numpy as np

class WeatherSimulation:
    def __init__(self,transition_probabilities,holding_times):
        self.transition_probabilities = transition_probabilities
        self.holding_times = holding_times
        #Checking probability is equal to 1 or not
        for i in self.transition_probabilities:
            if sum(self.transition_probabilities[i].values())!=1:
                raise RuntimeError("Sum of probabilites is not equal to 1 ")
        self.transition_names = []
        self.transition_prob = []
        self.temp_keys={}
        #creating array of transition probabilities
        for i in self.transition_probabilities:
            temp = []
            probs=[]
            self.temp_keys[i[:2]]=i
            for j in self.transition_probabilities[i]:
                temp.append(i[:2]+j[:2])
                probs.append(self.transition_probabilities[i][j])
            self.transition_names.append(temp)
            self.transition_prob.append(probs)
        self.cur_state = 'sunny'
        self.count = 1
    
    def get_states(self):
        '''
          function to get all the states
        '''
        return list(self.transition_probabilities.keys())
    
    def current_state(self):
        '''
          function to get the current state
        '''
        return self.cur_state
    
    def set_state(self,new_state):
        '''
            function to set the new state to current state
        '''
        self.cur_state = new_state
    
    def next_state(self):
        '''
            function to simulate for the next state using np.random.choice
        '''
        if self.current_state_remaining_hours()==0: #checking whether holding time for the curcrent state is satisfied
            self.count = 1
            predictedState = np.random.choice(self.transition_names[self.get_states().index(self.cur_state)],
                                  p=self.transition_prob[self.get_states().index(self.cur_state)])
            return self.temp_keys[predictedState[2:]]
        else:
            self.count+=1
            return self.cur_state
        
    def current_state_remaining_hours(self):
        '''
            function to get remaining holding time
        '''
        return self.holding_times[self.cur_state]-self.count
    
    def iterable(self):
        '''
            generator to yield the current state
        '''
        while True:
            temp = self.next_state()
            self.set_state(temp)
            yield self.cur_state
    
    def simulate(self,hours):
        '''
            function to simulate the weather based on given number of hours
        '''
        counts = {}
        for i in self.get_states():
            counts[i]=0
        for i in range(hours):
            state = self.next_state()
            self.set_state(state)
            counts[state]+=1
        total=sum(counts.values())
        out=[]
        for i in counts:
            out.append(counts[i]*100/total)
        return out
