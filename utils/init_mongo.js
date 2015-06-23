/**
 * Created by juancarlosfarah on 07/06/15.
 */

// Create Indexes
// ==============
function createIndexes() {
    var db = db.getSiblingDB("infotheoretic");
    db.oscillator_data.ensureIndex({ "simulation_id": -1, "_id": 1 });
}

// Remove Simulation Data
// =======================
function removeSimulationData(key) {
    var q = {};
    q[key] = true;
    var c = db.oscillator_simulation.find(q);

    while (c.hasNext()) {
        var doc = c.next();
        var sim_id = doc['_id'];
        db.oscillator_data.remove({"simulation_id": sim_id});
    }

    db.oscillator_simulation.remove(q);

}

// Copy Data
// =========
function duplicate() {
    var c = db.oscillator_simulation.find({"is_surrogate": true}, {"_id": 0});

    while (c.hasNext()) {
        var doc = c.next();
        doc["is_sorted"] = true;
        db.oscillator_data.insert(doc);
    }
}