# meerkatApp
Welcome to the Git-Hub repo for MK-2, the web-app that allows researchers interested in schizophrenia research to browse and export data from MeerKat, the former Cochrane Schizophrenia Group's study-based register. 

This repository contains Python/Streamlit code for the web-app that is currently deployed online and accessible here: [MK-2 website](http://16.171.210.179:8501/).

Code for the Python API that connects the web-app with an Elasticsearch cluster is in this Git repo: [MK-2 API](https://github.com/L-ENA/meerkatAPI)

## History and rationale

Reviews of studies of the effects of treatments have always been required to summarize evidence with authority.

This process began to be undertaken in a rigorous, reproducible – systematic - way in the 1970s but it was not until the advent of the Cochrane Collaboration in the 1990s that the process became ‘industrialized’.

In a systematic review of treatments great efforts are made to quantify the outcomes of the interventions and these numbers are extracted from published reports and then synthesized in the review.

Reviewers make great efforts to avoid multiple counting of individuals in studies who have had results of the same study reported in many publications and it is often difficult to determine the number randomized.

It became increasingly obvious to reviewers that

• the building block of the review was the study and not the report;

• that expensive efforts were made to curate multiple reports into representations of their parent studies;

• that these study-based data were used within the review only for the curated hard-won ‘parent’ study not to be made widely available;

• subsequent reviewers would have to repeat the process, recreating the study from the lengthening list of publications; and finally that

• although replication is important, waste within systematic review work was enormous.

In 2004 the UK Cochrane Centre supported Update Software with modest public funding to work with Information Specialists, and reviewers to create a more sophisticated study-based register system holding curated reports in groups of their parent studies. This relational database, built in MS Access, was named MeerKat.

Despite good functionality and support, this programme was not widely adopted across the Cochrane Collaboration. Only Renal and Schizophrenia of the then fifty Cochrane groups use this programme. There are many reasons why software is not adopted and why MeerKat was not widely used within Cochrane but poor functionality was not among them. MeerKat brought a positive step-change in the level of sophistication of information provision and, by supply of study-based data, an incalculable reduction in time wastage.

There are benefits to use of MS Access but these are now outweighed by the advantages of more online connectivity. MeerKat has to be renamed – there are many meerkats to be found on the internet – but is nevertheless reborn in this pilot, study-based register – MK-2. We hope you enjoy it, use it, and tell us how we can improve it.
