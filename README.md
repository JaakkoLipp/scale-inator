# Scale-inator
Perniöhedelmä palkkalaskuri
best MS-paint art:
![possibleplan](https://user-images.githubusercontent.com/46355010/123144712-a7aec900-d464-11eb-9ec2-39262f5c3c75.png)

# notes

core:  
- input data from serial (vaaka).  
- read koppa barcode with scanner.  
- koppas 1-5 to kerääjä1, 5-10 to kerääjä2.  
- Collectors have # of baskets. baskets have ID from 0-x.
- log both kg and kerääjä to excel in different columns.  
- log summer TOTAL KG of berry collectors (excel).  

additional:  
- web storage backup.    
- per day?  
- per day logging with python?  
- maybe also somehow compute which koppa is what kerääjä?  
- minimize chance to duplicate same berries in program.  


Files:  
mansikka.py main     
GUI.py GUI  
data.py csv / data storage  if need alot of code  

BARCODE END WITH EOL / LINEBREAK P SYMBOL TO GET AUTOMATIC ENTER ON READ  
-calculate totals as a summ on excel with specific collector IDs  

Needs Fixing:  
-kori ID assignment to specific collectors without massive ifelse, # of collectors big.  
-ID input requires Enter press

- 100 Collectors, up to 20 IDs per 1c
