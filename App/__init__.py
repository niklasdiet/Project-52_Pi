import configparser


# Check the in and outlets of the hub

# Open threads for the 2 reader and the other services

# Create matrix of the connected deviced
devices = [[('Hub', "xf273ge9fj"), ('CNC', "xr273re9fj"), ('CNC', "xr273re9fj")],
           [('Cobot', "xf273ge9fj"), ('Cobot', "xr273re9fj")],
           [('Cobot', "xf273ge9fj"), ('Cobot', "xr273re9fj"), ('Cobot', "xr273re9fj")]]




def systemCheck():
    print("System check started...")


    

if __name__ == "__main__":
    print("Starting App...")
    # get keys
    config = configparser.ConfigParser()
    config.read('Keys.cfg')
    cfgM = config['MONGODB']


