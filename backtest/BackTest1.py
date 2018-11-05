# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 17:11:39 2018

@author: diamond
"""

import bt
import pandas as pd

class StockSelection(bt.Algo):
    def __init__(self, activeStatus):
        self.signal = activeStatus
    
    def __call__(self, traget):
        # get signal on target.now
        if target.now in self.signal.index:
            sig = self.signal.ix[target.now]
            
            # get indices where true as list
            selected = list(sig.index[sig])
            
            #save in temp 
            target.temp['selected'] = selected
            
            
        return True
    

class StockWeight(bt.Algo):
    def __init__(self, target_weights):
        self.tw = target_weights
        
    def __call__(self,target):
        # get target weights on date target.now
        if target.now in self.tw.index:
            w = self.tw.ix[target.now]
            
            target.temp['weights'] = w.dropna()
            
        return True
    
class BackTestAPI(bt.Algo):
    def __init__(self):
        self.periods = ['Daily', 'Weekly', 'Monthly', 'Yearly']
        self.strat_p = [bt.algos.RunDaily(),
                        bt.algos.RunWeekly(),
                        bt.algos.RunMonthly(),
                        bt.algos.RunYearly()]
        self.result       = None
        self.positions    = {}
        self.transactions = {}
        
    def run(self, data, strats):
        ''' data   : DataFrame with index as the dates, and the columns are the 
                     stocks' prices
            strats : a dictionary of all strategies in the form of 
                    {'strategyName':
                        {   'weights': DataFrame of weights,
                            'period' : 'Daily', 'Weekly', 'Monthly', 'Yearly' (this one is Daily as default)
                        }
                    }
            In each strats, the weights are the weights of the allocated capital of the fund. 
            For example, one fund has $100M capital initially, 
            On Day 1, invest IBM $20M, JPM $50M, then the weight is IBM: 20%, JPM: 50%
                Assume on Day 1, the fund profits $20M, then the fund has $120 capital
            On Day 2, invest IBM $120M, short JPM $120M, then the weight is IBM: 100%, JPM: -100%
            The other days' weights are using the same manner. This will generate the real PnL 
            of the fund realized during the investment. 
        '''
        strategyList = []
        
        for sName, sStrat in strats.items():
            strat_p = self.strat_p[self.periods.index(sStrat.get('period','Daily'))]
            weight  = sStrat['weight']
            s       = bt.Strategy(sName,  [strat_p,
                                           bt.algos.SelectAll(),
                                           StockWeight(weight),
                                           bt.algos.Rebalance()]
                                  )
            strategyList += [bt.Backtest(s, data)]
        
        res  = bt.run(*strategyList)
        self.result = res
        
        for i in list(strats.keys()):           
            print (i)
            self.transactions[i] = res.get_transactions(i).reset_index().pivot_table('quantity','Date', 'Security')
            self.positions[i]    = self.transactions[i].cumsum()
        
        return res
    
    
    def display(self, strategy=None):
        ''' display the backtest result of a given strategy or 
            a list of strategies or all strategies
            strategy: a list of a strategy, all strategies as the default
        '''
        res = self.result
        
        res.display()
        print(res.plot_correlation(title = 'Strategies Return Correlation'))
        print(res.plot_scatter_matrix())
        
        if strategy is None:
            strategy = list(self.result) 
        
        print(res.prices[strategy].plot(title='BackTester', grid=True, figsize = [15,5]))
        
        for i in strategy:
            print(self.transactions[i].iloc[1:,:].plot(title='Transaction for '+ i, grid=True, figsize = [15,5]))
            print(self.positions[i].plot(title='Position for '+ i, grid=True, figsize = [15,5]))
            print(res.get_weights(i).iloc[1:,1:].plot(title ='Dynamic Allocation for '+i, grid =True, figsize = [15,5]))
            print(res.plot_histogram(i,grid=True, figsize=[15,5]))
            
        print(res.lookback_returns.iloc[::-1][strategy].plot(title='LookBack Performance', kind='Bar',grid=True, figsize =[15,5]))
        
        
        
        
#===========================================================================''
#     Below are the test files
#===========================================================================        
        
data = bt.get('aapl, c, ge, gs, msft', start='2010-01-01')        

wt = data.copy()

wt['aapl'] = 0.1
wt['msft'] = 0.2
wt['ge']   = 0.2
wt['gs']   = 0.2
wt['c']    = 0.3

strats = {'s1':{'weight': wt},
          's2':{'weight': wt*0.5}
         }

obj = BackTestAPI()

res = obj.run(data, strats)

obj.display()
        
        
        
        
        
        
        
        
        
        
        
        
        