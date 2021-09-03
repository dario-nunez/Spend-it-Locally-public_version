/*
This file contains color information used in the application.
 */
const blankPathFill = "#000000";
let borderColor = "#000000"

// Red - Green - Scale min and max values.
let continuousLinearLow = [240, 100, 36];
let continuousLinearHigh = [0, 100, 36];

/*
Color mappings for the specific datasets in the original data folder of this project. The keys match the encoding system
applied in the "output_data_metadata" file.
*/
const colourMappingsSimple = {
    "household": {
        "category": {
            "1. Affluent Achievers": {
                "colour": "#304dec",
                "name": "1. Affluent Achievers",
            },
            "2. Rising Prosperity": {
                "colour": "#7d38ba",
                "name": "2. Rising Prosperity"
            },
            "3. Comfortable Communities": {
                "colour": "#4f9342",
                "name": "3. Comfortable Communities"
            },
            "4. Financially Stretched": {
                "colour": "#f47421",
                "name": "4. Financially Stretched"
            },
            "5. Urban Adversity": {
                "colour": "#00a1c5",
                "name": "5. Urban Adversity"
            },
            "6. Not Private Households": {
                "colour": "#e44296",
                "name": "6. Not Private Households"
            },
            "undefined": {
                "colour": "#000000",
                "name": "undefined"
            },
            "other": {
                "colour": "#000000",
                "name": "other"
            }
        },
        "group": {
            "A. Lavish Lifestyles": {
                "colour": "#304dec",
                "name": "A. Lavish Lifestyles",
                "children": [1,3]
            },
            "B. Executive Wealth": {
                "colour": "#6276f0",
                "name": "B. Executive Wealth",
                "children": [4,9]
            },
            "C. Mature Money": {
                "colour": "#a7b2f7",
                "name": "C. Mature Money",
                "children": [10,13]
            },
            "D. City Sophisticates": {
                "colour": "#7d38ba",
                "name": "D. City Sophisticates",
                "children": [14,17]
            },
            "E. Career Climbers": {
                "colour": "#a572d4",
                "name": "E. Career Climbers",
                "children": [18,20]
            },
            "F. Countryside Communities": {
                "colour": "#4f9342",
                "name": "F. Countryside Communities",
                "children": [21,23]
            },
            "G. Successful Suburbs": {
                "colour": "#74ba66",
                "name": "G. Successful Suburbs",
                "children": [24,26]
            },
            "H. Steady Neighbourhoods": {
                "colour": "#99cd8f",
                "name": "H. Steady Neighbourhoods",
                "children": [27,29]
            },
            "I. Comfortable Seniors": {
                "colour": "#b2daaa",
                "name": "I. Comfortable Seniors",
                "children": [30,31]
            },
            "J. Starting Out": {
                "colour": "#dce9d7",
                "name": "J. Starting Out",
                "children": [32,33]
            },
            "K. Student Life": {
                "colour": "#f47421",
                "name": "K. Student Life",
                "children": [34,36]
            },
            "L. Modest Means": {
                "colour": "#f79e64",
                "name": "L. Modest Means",
                "children": [37,40]
            },
            "M. Striving Families": {
                "colour": "#fac8a7",
                "name": "M. Striving Families",
                "children": [41,44]
            },
            "N. Poorer Pensioners": {
                "colour": "#fde3d2",
                "name": "N. Poorer Pensioners",
                "children": [45,48]
            },
            "O. Young Hardship": {
                "colour": "#00a1c5",
                "name": "O. Young Hardship",
                "children": [49,51]
            },
            "P. Struggling Estates": {
                "colour": "#4dbdd5",
                "name": "P. Struggling Estates",
                "children": [52,56]
            },
            "Q. Difficult Circumstances": {
                "colour": "#99d8e9",
                "name": "Q. Difficult Circumstances",
                "children": [57,59]
            },
            "R. Active Communal Population": {
                "colour": "#e44296",
                "name": "R. Active Communal Population",
                "children": [60,62]
            },
            "undefined": {
                "colour": "#000000",
                "name": "undefined"
            },
            "other": {
                "colour": "#000000",
                "name": "other"
            }
        }
    },
    "wellbeing": {
        "group": {
            "1. Health Challenges": {
                "colour": "#38329a",
                "name": "1. Health Challenges",
            },
            "2. At Risk": {
                "colour": "#89756e",
                "name": "2. At Risk",
            },
            "3. Caution": {
                "colour": "#304ba0",
                "name": "3. Caution",
            },
            "4. Healthy": {
                "colour": "#c1c740",
                "name": "4. Healthy",
            },
            "5. Not Private Households": {
                "colour": "#563b97",
                "name": "5. Not Private Households",
            },
            "undefined": {
                "colour": "#000000",
                "name": "undefined",
            }
        },
        "type": {
            "1. Limited living" : {
                "colour": "#38329a",
                "name": "1. Limited living",
            },
            "2. Poorly pensioners" : {
                "colour": "#38329a",
                "name": "2. Poorly pensioners",
            },
            "3. Hardship heartlands" : {
                "colour": "#38329a",
                "name": "3. Hardship heartlands",
            },
            "4. Elderly ailments" : {
                "colour": "#38329a",
                "name": "4. Elderly ailments",
            },
            "5. Countryside complacency" : {
                "colour": "#38329a",
                "name": "5. Countryside complacency",
            },
            "6. Dangerous dependencies" : {
                "colour": "#89756e",
                "name": "6. Dangerous dependencies",
            },
            "7. Struggling smokers" : {
                "colour": "#89756e",
                "name": "7. Struggling smokers",
            },
            "8. Despondent diversity" : {
                "colour": "#89756e",
                "name": "8. Despondent diversity",
            },
            "9. Everyday excesses" : {
                "colour": "#89756e",
                "name": "9. Everyday excesses",
            },
            "10. Respiratory risks" : {
                "colour": "#89756e",
                "name": "10. Respiratory risks",
            },
            "11. Anxious adversity" : {
                "colour": "#89756e",
                "name": "11. Anxious adversity",
            },
            "12. Perilous futures" : {
                "colour": "#89756e",
                "name": "12. Perilous futures",
            },
            "13. Regular revellers" : {
                "colour": "#89756e",
                "name": "13. Regular revellers",
            },
            "14. Rooted routines" : {
                "colour": "#304ba0",
                "name": "14. Rooted routines",
            },
            "15. Borderline behaviours" : {
                "colour": "#304ba0",
                "name": "15. Borderline behaviours",
            },
            "16. Countryside concerns" : {
                "colour": "#304ba0",
                "name": "16. Countryside concerns",
            },
            "17. Everything in moderation" : {
                "colour": "#304ba0",
                "name": "17. Everything in moderation",
            },
            "18. Cultural concerns" : {
                "colour": "#304ba0",
                "name": "18. Cultural concerns",
            },
            "19. Relishing retirement" : {
                "colour": "#c1c740",
                "name": "19. Relishing retirement",
            },
            "20. Perky pensioners" : {
                "colour": "#c1c740",
                "name": "20. Perky pensioners",
            },
            "21. Sensible seniors" : {
                "colour": "#c1c740",
                "name": "21. Sensible seniors",
            },
            "22. Gym & juices" : {
                "colour": "#c1c740",
                "name": "22. Gym & juices",
            },
            "23. Happy families" : {
                "colour": "#c1c740",
                "name": "23. Happy families",
            },
            "24. Five-a-day greys" : {
                "colour": "#c1c740",
                "name": "24. Five-a-day greys",
            },
            "25. Healthy, wealthy & wine" : {
                "colour": "#c1c740",
                "name": "25. Healthy, wealthy & wine",
            },
            "26. Active communal population": {
                "colour": "#563b97",
                "name": "26. Active communal population",
            },
            "27. Inactive communal population": {
                "colour": "#563b97",
                "name": "27. Inactive communal population",
            },
            "28. Business addresses etc.": {
                "colour": "#563b97",
                "name": "28. Business addresses etc.",
            },
            "undefined": {
                "colour": "#000000",
                "name": "undefined",
            }
        }
    },
    "PTAL":{
        "default":{
            "6b": {
                "colour": "#b62419",
                "name": "6b"
            },
            "6a": {
                "colour": "#ff3f35",
                "name": "6a"
            },
            "5": {
                "colour": "#ff8972",
                "name": "5"
            },
            "4": {
                "colour": "#f2e33f",
                "name": "4"
            },
            "3": {
                "colour": "#0dae4e",
                "name": "3"
            },
            "2": {
                "colour": "#85dce3",
                "name": "2"
            },
            "1b": {
                "colour": "#72b4e0",
                "name": "1b"
            },
            "1a": {
                "colour": "#142d72",
                "name": "1a"
            },
            "": {
                "colour": "#000000",
                "name": "blank"
            }
        }
    },
    "street_value" : {

    }
}
