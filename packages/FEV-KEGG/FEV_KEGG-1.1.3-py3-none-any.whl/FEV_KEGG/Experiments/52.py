"""
Context
-------
In :mod:`49`, we did this before, but this time we export into pretty HTML.

Question
--------
Which neofunctionalised enzymes cause the core metabolism of Deltaproteobacteria to have increased redundancy? How much do they contribute?
Grouped by contributed functions, sorted lexicographically, annotated with links to KEGG, annotated with human-readable names (if possible), and exported into an HTML file.

Method
------
- get clade
- get core metabolism
- calculate "neofunctionalised" ECs
- calculate redundancy
- REPEAT for each "neofunctionalised" EC contributing to redundancy
-     report enzyme pairs of neofunctionalisations, which caused the EC to be considered "neofunctionalised", and are in return contributing to redundancy
-     print them into nice HTML

Result
------

::

    core metabolism majority: 80%
    neofunctionalisation majority: 0% (this means that gene duplication within a single organism is enough)
    
    Deltaproteobacteria:
    
    core metabolism ECs: 228
    
    "neofunctionalised" ECs: 36 (16%)
    
    Neofunctionalisations contributing to robustness: 84
    
    [see file Deltaproteobacteria_ROBUSTNESS_Neofunctionalisations-For-Contributed-EC.html]
    

Conclusion
----------
Much more useful than a plain text list of cryptic IDs.

The well-known neofunctionalisation 2.6.1.1 <-> 2.6.1.9 does not occur here. 
Maybe the core metabolism's majority percentage is too high, or both of the two EC numbers can only contribute to partial redundancy?
"""

from FEV_KEGG.KEGG.File import cache
from FEV_KEGG.Evolution.Clade import Clade
from FEV_KEGG.Statistics import Percent
from FEV_KEGG.Robustness.Topology.Redundancy import RedundancyType, Redundancy, RedundancyContribution
from FEV_KEGG import settings
from FEV_KEGG.Util.Util import dictToHtmlFile

@cache(folder_path='experiments', file_name='deltaproteobacteria_clade')
def getCladeA():
    clade = Clade('Deltaproteobacteria')
    # pre-fetch collective metabolism into memory
    clade.collectiveMetabolism(excludeMultifunctionalEnzymes=settings.defaultNoMultifunctional)
    # pre-fetch collective enzyme metabolism into memory
    clade.collectiveMetabolismEnzymes(excludeMultifunctionalEnzymes=settings.defaultNoMultifunctional)
    return clade

if __name__ == '__main__':

    output = ['']

    #- get clade
    clade = getCladeA()
    majorityPercentageCoreMetabolism = 80
    majorityPercentageNeofunctionalisation = 0
    
    redundancyType = RedundancyType.ROBUSTNESS
    
    output.append( 'core metabolism majority: ' + str(majorityPercentageCoreMetabolism) + '%' )
    output.append( 'neofunctionalisation majority: ' + str(majorityPercentageNeofunctionalisation) + '% (this means that gene duplication within a single organism is enough)' )
    output.append('')
    output.append(', '.join(clade.ncbiNames) + ':')
    output.append('')
    
    #- get core metabolism
    cladeEcGraph = clade.coreMetabolism(majorityPercentageCoreMetabolism)
    cladeEcCount = len(cladeEcGraph.getECs())
    output.append( 'core metabolism ECs: ' + str(cladeEcCount) )
    output.append('')
    
    #- calculate "neofunctionalised" ECs
    cladeNeofunctionalisedMetabolismSet = clade.neofunctionalisedECs(majorityPercentageCoreMetabolism, majorityPercentageNeofunctionalisation).getECs()
    cladeNeofunctionalisationsForFunctionChange = clade.neofunctionalisationsForFunctionChange(majorityPercentageCoreMetabolism, majorityPercentageNeofunctionalisation)
    
    #- calculate redundancy
    cladeRedundancy = Redundancy(cladeEcGraph)
    cladeRedundancyContribution = RedundancyContribution(cladeRedundancy, cladeNeofunctionalisedMetabolismSet)
    
    cladeRobustnessContributedECsForContributingNeofunctionalisedEC = cladeRedundancyContribution.getContributedKeysForSpecial(redundancyType)
    cladeRobustnessContributingNeofunctionalisedECs = set(cladeRobustnessContributedECsForContributingNeofunctionalisedEC.keys())
    
    #- REPEAT for each function change consisting of "neofunctionalised" ECs, which also contribute to redundancy
    output.append( '"neofunctionalised" ECs: ' + str(len(cladeNeofunctionalisedMetabolismSet)) + ' (' + str(Percent.getPercentStringShort(len(cladeNeofunctionalisedMetabolismSet), cladeEcCount, 0)) + '%)' )
    
    robustnessContributingNeofunctionalisations = dict()
    
    for functionChange, neofunctionalisations in cladeNeofunctionalisationsForFunctionChange.items():
        #-     report enzyme pairs of neofunctionalisations, which caused the EC to be considered "neofunctionalised", and are in return contributing to redundancy        
        
        if functionChange.ecA in cladeRobustnessContributingNeofunctionalisedECs or functionChange.ecB in cladeRobustnessContributingNeofunctionalisedECs: # function change contributes to robustness
            
            for neofunctionalisation in neofunctionalisations:
                currentSetOfContributedECs = robustnessContributingNeofunctionalisations.get(neofunctionalisation, None)
                
                if currentSetOfContributedECs is None:
                    currentSetOfContributedECs = set()
                    robustnessContributingNeofunctionalisations[neofunctionalisation] = currentSetOfContributedECs
                
                for ec in functionChange.ecPair:
                    contributedECs = cladeRobustnessContributedECsForContributingNeofunctionalisedEC.get(ec, None)
                    if contributedECs is not None:
                        currentSetOfContributedECs.update(contributedECs)
    
    output.append('')
    output.append( 'Neofunctionalisations contributing to robustness: ' + str(len(robustnessContributingNeofunctionalisations)) )
    
    
    neofunctionalisationsForContributedEC = dict()
    for neofunctionalisation, contributedECs in robustnessContributingNeofunctionalisations.items():
        
        for contributedEC in contributedECs:
            
            currentSetOfNeofunctionalisations = neofunctionalisationsForContributedEC.get(contributedEC, None)
            
            if currentSetOfNeofunctionalisations is None:
                currentSetOfNeofunctionalisations = set()
                neofunctionalisationsForContributedEC[contributedEC] = currentSetOfNeofunctionalisations
                
            currentSetOfNeofunctionalisations.add(neofunctionalisation)
    
    
    ecNumbers = set()
    for contributedEC in neofunctionalisationsForContributedEC.keys():
        ecNumbers.add( contributedEC )
    
    dictToHtmlFile(neofunctionalisationsForContributedEC, clade.ncbiNames[0] + '_' + redundancyType.name + '_Neofunctionalisations-For-Contributed-EC.html', byValueFirst=False, inCacheFolder=True, addEcDescriptions = ecNumbers)
  
    
    
    
    
    
    for line in output:
        print( line )
