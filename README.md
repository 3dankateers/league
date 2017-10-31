# league


Big Picture:                                                                                                                  
We want to reliably profit via betting on the outcome of professional league of legends matches. This is typically done       
by placing a bet against the market determined odds. If the market determined odds are inefficient, aka differ substantially from the "true" odds, there is a potential to make money. One only needs to calculate better odds than the market and place bet accordingly.                           
                                                                                                                                                                                                                                                         
Assumptions:
1. The "true odds" are determined by a wide variety of factors such as team's past performance, etc + natural variance. 
2. The market determined odds prior to champions being locked in encapsulates the information from most of these factors.
3. The market odds do not change substantially after champion lockins(empirical evidence for this).
4. A bet determined by flipping a coin has expected value of -(service fees). As a matter of fact if this yielded a bigger negative expected value than service fees, then we would simply flip our choice and get positive expected value(obv false).


Concept:
From Ass 1 + 2 + 3, 2 possibilities follow. Either champion lockins are not a major factor determining "true odds" in which case we're fucked and no money can be made or the market is inefficiently processing this factor and the odds should change but the market did not react. If the latter is true, the market odds immediately after champion lockins are inefficient and money can be made by taking into account lockins. Using Ass 4, a stronger statement can be made, we ONLY have to take into account champion lockins to decide whether to bet and on what side and as long as champion lockins are a big enough factor to counter-act service fee, then we can elevate the expected value of a bet to a positive number.
                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                              
Details:      
In practice, it is quite difficult to take into account champion lockins(team comp). Most likely we will create specific "indicators" that use the champion lockin information partially. For example, an ally-pair indicator could aggregate the win% of pairs of champs on the same team and learn which champs work well together. Another indicator could look at ally-enemy matchups and do something similar. These indicators could be combined(tricky since there is internal correlation) to get a prediction rate that is as high as possible. Linear regression might be helpful here.
                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                              
Instructions:                                                                                                                 
1. Get WSL working so you can use linux bash : https://msdn.microsoft.com/en-us/commandline/wsl/install-win10                 
2. Setup bash                                                                                                                 
3. from .../league/ run "make all"                                                                                            
4. Install required python packages:<br />                                                                                    
        pip install pymongo <br />                                                                                            
        pip install retrying <br />                                                                                           
        pip install numpy <br />                                                                                              
        pip install -U statsmodels <br />                                                                                     
        pip install sklearn <br />                                                                                            
                                                                                                                              
Running local Mongodb                                                                                                         
1.                                                                                                                            
