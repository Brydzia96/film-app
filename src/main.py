import os
import sqlite3
import website
import typer

from rich import print 
from rich.console import Console
from rich.table import Table

console = Console()

def get_info():
    #Getting data from user
    film_title = typer.prompt("Enter film name")
    
    #film_title = "Avatar the way of water"   
    film_year = typer.prompt("Enter film year")
    film_year = str(film_year)
    return film_title, film_year

def get_values(film_title, film_year):
    imdb = website.Imdb(film_title, film_year)
    imdb.get_score()
    rotten = website.RottenTomatoes(film_title, film_year)
    rotten.get_score()
   
    ask = typer.prompt("Would you like to save the data or just display the result? y/n")
    if ask == "y":
        return imdb, rotten
    elif ask == "n":
        print(f"Title: {film_title}, Year: {film_year}, IMDB score: {imdb.score}, Rotten audience score: {rotten.audience_score}")
        return None, None
    else:
        print("No valid input")
        return None, None

def add_to_database(film_title, film_year, imdb, rotten):
    con = sqlite3.connect("film.db")
    cur = con.cursor()

    #cur.execute("CREATE TABLE film(title, year, imdb_score, rotten_score)")

    cur.execute(f"""
    INSERT INTO film VALUES
     ('{film_title}', '{film_year}', '{imdb.score}', '{rotten.audience_score}') """)
      
    con.commit()
    con.close()

def retrieve_from_database():
    con = sqlite3.connect("film.db")
    cur = con.cursor()
    table = Table("Year", "Title", "IMBD score", "Rotten audience score" )

    for row in cur.execute("SELECT year, title, imdb_score, rotten_score FROM film ORDER BY year"):
        #print(row)
        table.add_row(row[0], row[1], row[2], row[3])

    con.close()   
    console.print(table)

def main():
    film_title, film_year = get_info()
    imdb, rotten = get_values(film_title, film_year)

    if imdb:
        add_to_database(film_title, film_year, imdb, rotten)

    sort = typer.prompt("Would you like to display the year sorted film table? y/n")
    if sort == "y":
        retrieve_from_database()
    elif sort == "n":
        print("Have a good day :) Bye")
    else:
        print("I didn't get it. See you later")
 
   
if __name__ == "__main__":
    typer.run(main)
    

    
    






            


        
        

    
    
    