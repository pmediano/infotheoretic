__author__ = 'juancarlosfarah'

import oct2py
import os
import pymongo
import numpy as np
from bson.objectid import ObjectId


class OscillatorDataImporter:

    def __init__(self, database=None):
        self.db = database

        pass

    def connect(self, database):
        """
        Connect to MongoDB database.
        :param database: Database name.
        :return: Handle to database.
        """
        host = "localhost"
        port = 27017
        mc = pymongo.MongoClient(host=host, port=port)
        self.db = mc.get_database(database)
        return self.db

    def load_folder(self, folder, threshold):
        if not os.path.isdir(folder):
            raise NameError(folder)

        files = os.listdir(folder)

        # Files are by default Octave files.
        # Initialise Oct2Py object.
        oc = oct2py.Oct2Py()

        for f in files:
            path = folder + "/" + f
            output = oc.load(path)
            sync = output.data.sync
            duration = len(sync)
            num_oscillators = sync[0].shape[0]
            avg_syncs = []
            beta = output.data.b
            sync_discrete = []
            syncs = np.zeros((num_oscillators, duration))

            # Create ObjectId
            _id = ObjectId()

            t_step = 0
            for sync_t in sync:

                # Record average synchrony to calculate global synchrony.
                avg_sync_t = np.average(sync_t)
                avg_syncs.append(avg_sync_t)

                # Get diagonal and store for later calculations.
                diagonal = sync_t.diagonal().copy()
                syncs[:, t_step] = diagonal.T

                # Transform diagonal.
                diagonal[diagonal < threshold] = 0
                diagonal[diagonal >= threshold] = 1

                # Store information in object.
                sync_obj = {
                    "simulation_id": _id,
                    "data": diagonal.tolist()
                }
                sync_discrete.append(sync_obj)
                t_step += 1

            # Compute variance for lambda.
            sync_vars = []
            for i in range(num_oscillators):
                sync_vars.append(np.var(syncs[i]))

            # Compute variance for chi.
            chi_vars = []
            for i in range(duration):
                chi_vars.append(np.var(syncs[:, i]))

            lamda = np.average(sync_vars)
            chi = np.average(chi_vars)
            avg_sync = np.average(avg_syncs)

            obj = {
                "_id": _id,
                "global_sync": avg_sync,
                "beta": beta,
                "lambda": lamda,
                "chi": chi,
                "num_oscillators": num_oscillators,
                "duration": duration,
                "threshold": threshold
            }

            # Storing in MongoDB if database has been defined.
            db = self.db
            if db is not None:
                db.oscillator_simulation.insert_one(obj)
                db.oscillator_data.insert(sync_discrete)

        return

if __name__ == '__main__':
    data_folder = "/Users/juancarlosfarah/Git/data/Data"
    default_db = "individual_project"

    # odi = OscillatorDataImporter()
    # odi.connect(default_db)
    # odi.load_folder(data_folder, 0.9)
    # odi.load_folder(data_folder, 0.8)
    # odi.load_folder(data_folder, 0.7)
    # odi.load_folder(data_folder, 0.6)
    # odi.load_folder(data_folder, 0.5)