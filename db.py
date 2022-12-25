
import sys
import sqlite3 as sql
import csv
from matplotlib import pyplot as plt

class Database():
    def __init__(self,url):
        super().__init__()
        # Create a database file named db
        self.db = sql.connect("data.db")
        # Define database cursor
        self.cur = self.db.cursor()
        # Create table in database
        self.cur.execute("CREATE TABLE IF NOT EXISTS StrainStress (Strain real, Stress real);")

        self.addData(url)
        self.delNegative()
        
        self.int_TS = None
        self.EM = None
        
        self.tensile_strength()
        self.elastic_modulus()


    def addData(self,url):
        """Add raw data to database"""

        # Take the values in csv file and transfer to db
        with open(url) as file:
            dr = csv.DictReader(file)
            to_db = [(i['Strain'], i['Stress']) for i in dr]
        self.cur.executemany("INSERT INTO StrainStress (Strain, Stress) VALUES (?, ?);", to_db)
        self.db.commit()


    def delNegative(self):
        """Delete negative values in strain data, together with stress data"""

        # Delete negative strain values in db
        self.cur.execute("DELETE FROM StrainStress WHERE Strain<0;")
        self.db.commit()


    def tensile_strength(self):
        """Find Tensile Strength in database"""

        # Find maximum stress value in db
        TS = self.cur.execute("SELECT MAX(Stress) from StrainStress;").fetchone()
        self.int_TS = TS[0]


    def elastic_modulus(self):
        """Calculate Elastic Modulus in 0.003-strain region according to ASTM D3039"""
        
        # Find stress values at 0.003 and 0.001 strain limits
        YS1 = self.cur.execute("SELECT MAX(Stress) from StrainStress WHERE Strain <= 0.003;").fetchone()
        YS2 = self.cur.execute("SELECT MIN(Stress) from StrainStress WHERE Strain >= 0.001;").fetchone()
        
        # Find strain values close to 0.003 and 0.001 strain limits
        strain1 = self.cur.execute("SELECT MAX(Strain) from StrainStress WHERE Strain <= 0.003;").fetchone()
        strain2 = self.cur.execute("SELECT MIN(Strain) from StrainStress WHERE Strain >= 0.001;").fetchone()
        
        # Find stress and strain differences
        int_YS = YS1[0]-YS2[0]
        int_strain = strain1[0]-strain2[0]

        # Calculate elastic modulus
        self.EM = (int_YS/int_strain)/1000 #gives elastic modulus in GPa


    def plot(self):
        """Plot stress vs. strain curve of the data"""
        
        # Select all data from database and make a list of them
        self.cur.execute("SELECT Strain, Stress from StrainStress")
        rs = self.cur.fetchall()

        # Define two lists for stress and strain for plot axes
        strain = []
        stress = []

        # Fill out the list with stress and strain data
        for row in rs:
            strain.append(row[0])
            stress.append(row[1])
        
        # Make plot
        # plt.get_current_fig_manager().canvas.set_window_title('Results')
        plt.title("Normalized Stress vs. Strain Curve")
        plt.scatter(strain, stress, color='darkblue', marker='o', s=2)

        plt.xlabel("Strain (%)")
        plt.ylabel("Stress (MPa)")

        plt.show()

    def fetchall(self):
        """Plot stress vs. strain curve of the data"""
        
        # Select all data from database and make a list of them
        self.cur.execute("SELECT Strain, Stress from StrainStress")
        rs = self.cur.fetchall()

        # Define two lists for stress and strain for plot axes
        strain = []
        stress = []

        # Fill out the list with stress and strain data
        for row in rs:
            strain.append(row[0])
            stress.append(row[1])
        
        return strain, stress


if __name__ == '__main__':
    app = sql(sys.argv)
    ex = App()
    sys.exit(app.exec_())