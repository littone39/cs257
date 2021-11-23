AUTHORS: Jayti Arora, Emily Litton

DATA: World Happiness Report 2005-2021. Includes information from Gallup Poll about
country happiness (life ladder), gdp, social support, and other related quality of life 
statistics over time.

STATUS: Users can view data for a single country on the 'Map' page by clicking a country 
on the map or selecting one from the drop down menu. The data displayed is from the most 
recent year and then there is a small graph that shows happiness over time. Users can also 
create a scatter plot comparing happiness score to another variable on the page titled 
[CHANGE TO PAGE NAME]. Navigation works and home/about pages provide additional information. 
All features are working.

NOTES: there are a few small quirks/things we couldn't figure out:
    - the graph axes don't start at zero which is kind of weird and couldn't figure
    out in a reasonable amount of time how to fix it. 
    - name of the graph page isn't quite right -- we tried lots of different things but 
    none of them quite fit.   
    - api endpoint for about page should be /about but instead is /about-us because for 
    some reason /about always results in error 404.
