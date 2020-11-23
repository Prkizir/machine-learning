from pysc2.agents import base_agent
from pysc2.lib import actions, features, units
from pysc2.env import sc2_env, run_loop
from absl import app

import random, time

class TerranAgent(base_agent.BaseAgent):

    def init(self):
        super(TerranAgent, self).init()
        self.attack_coordinates = None

    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
            return True
        if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
            return True
        return False

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units if unit.unit_type == unit_type]

    def can_do(self, obs, action):
        return action in obs.observation.available_actions

    def build_refinery(self, obs):
        neutral_vespene_geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
        refineries = self.get_units_by_type(obs, units.Terran.Refinery)

        if len(refineries) < 1 and len(neutral_vespene_geysers) > 0:
            if self.unit_type_is_selected(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_Refinery_screen.id):
                    geyser = random.choice(neutral_vespene_geysers)
                    return actions.FUNCTIONS.Build_Refinery_screen("now", (geyser.x, geyser.y))

            scvs = self.get_units_by_type(obs, units.Terran.SCV)

            if len(scvs) > 0:
                scv = random.choice(scvs)
                return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))

    def gather_vespene_gas(self,obs):
        refinery = self.get_units_by_type(obs, units.Terran.Refinery)
        if len(refinery) > 0:
            refinery = random.choice(refinery)
            if refinery['assigned_harvesters'] < 3:
                if self.unit_type_is_selected(obs, units.Terran.SCV):
                    if len(obs.observation.single_select) < 2 and len(obs.observation.multi_select) < 2 :
                        if self.can_do(obs,actions.FUNCTIONS.Harvest_Gather_screen.id):
                            return actions.FUNCTIONS.Harvest_Gather_screen("now",(refinery.x, refinery.y))


                scvs = self.get_units_by_type(obs, units.Terran.SCV)
                if len(scvs) > 0 :
                    scv = random.choice(scvs)
                    return actions.FUNCTIONS.select_point("select",(scv.x,scv.y))


    def step(self, obs):
        super(TerranAgent, self).step(obs)

        if obs.first():
            # CHECK SELF POSITION
            player_y, player_x = (obs.observation.feature_minimap.player_relative == features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()

            # CHECK ENEMY POSITION
            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (49, 49)
            else:
                self.attack_coordinates = (12, 16)


        minerals = obs.observation.player.minerals

        # CREATE SUPPLY DEPOTS IN EVERY OPPORTUNITY (TO HAVE 3 IN TOTAL)
        SupplyDepot = self.get_units_by_type(obs, units.Terran.SupplyDepot)
        if len(SupplyDepot) < 3 and minerals >= 100:
            if self.unit_type_is_selected(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x, y))

        # CREATE BARRACKS IN EVERY OPPORTUNITY (TO HAVE 3 IN TOTAL)
        Barracks = self.get_units_by_type(obs, units.Terran.Barracks)
        if len(Barracks) < 3 and minerals >= 150:
            if self.unit_type_is_selected(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    return actions.FUNCTIONS.Build_Barracks_screen("now", (x, y))

        # ATTACK - MARINES (15 GROUP)
        Marines = self.get_units_by_type(obs, units.Terran.Marine)
        if len(Marines) >= 10:
            if self.unit_type_is_selected(obs, units.Terran.Marine):
                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                    return actions.FUNCTIONS.Attack_minimap("now", self.attack_coordinates)
            if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                return actions.FUNCTIONS.select_army("select")


        # CREATE MARINES
        if len(Barracks) >= 3:
            if self.unit_type_is_selected(obs, units.Terran.Barracks):
                Marines = self.get_units_by_type(obs, units.Terran.Marine)
                if len(Marines) <= 15:
                    if self.can_do(obs, actions.FUNCTIONS.Train_Marine_quick.id):
                        return actions.FUNCTIONS.Train_Marine_quick("now")
            b = random.choice(Barracks)
            return actions.FUNCTIONS.select_point("select_all_type", (b.x, b.y))

        b_refinery = self.build_refinery(obs)
        if b_refinery:
            return b_refinery

        # RECOLECTORS
        Recolectors = self.get_units_by_type(obs, units.Terran.SCV)
        if len(Recolectors) > 0:
            scv = random.choice(Recolectors)
            return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))

        g_refinery = self.gather_vespene_gas(obs)
        if g_refinery:
            return g_refinery

        return actions.FUNCTIONS.no_op()

class ZergAgent(base_agent.BaseAgent):

    def __init__(self):
        super(ZergAgent, self).__init__()
        self.attack_coordinates = None
        self.safe_coordinates = None

    """
    Utility Functions
    """

    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
            return True
        if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
            return True
        return False

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units if unit.unit_type == unit_type]

    def can_do(self, obs, action):
        return action in obs.observation.available_actions

    """
    Launch Attack Sequences
    """
    def launch_attack(self, obs):
        zerglings = self.get_units_by_type(obs, units.Zerg.Zergling)
        roaches = self.get_units_by_type(obs, units.Zerg.Roach)

        if len(roaches) >= 5 or len(zerglings) >= 10:
            if self.unit_type_is_selected(obs, units.Zerg.Zergling):
                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                    return actions.FUNCTIONS.Attack_minimap("now", self.attack_coordinates)

            if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                return actions.FUNCTIONS.select_army("select")

    """
    Structures
    """
    def build_spawning_pool(self, obs):

        """
        Spawning Pool
        """
        spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
        if len(spawning_pools) == 0:
            if self.unit_type_is_selected(obs, units.Zerg.Drone):
                if self.can_do(obs, actions.FUNCTIONS.Build_SpawningPool_screen.id):
                    x = random.randint(0, 50)
                    y = random.randint(0, 50)

                    return actions.FUNCTIONS.Build_SpawningPool_screen("now", (x, y))

            drones = self.get_units_by_type(obs, units.Zerg.Drone)

            if len(drones) > 0:
                drone = random.choice(drones)
                return actions.FUNCTIONS.select_point("select_all_type", (drone.x, drone.y))

    def build_roach_warren(self, obs):

        """
        Roach Warren
        """
        spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
        if len(spawning_pools) == 1:
            roach_warrens = self.get_units_by_type(obs, units.Zerg.RoachWarren)
            if len(roach_warrens) == 0:
                if self.unit_type_is_selected(obs, units.Zerg.Drone):
                    if self.can_do(obs, actions.FUNCTIONS.Build_RoachWarren_screen.id):
                        x = random.randint(0, 50)
                        y = random.randint(0, 50)

                        return actions.FUNCTIONS.Build_RoachWarren_screen("now", (x, y))

                drones = self.get_units_by_type(obs, units.Zerg.Drone)

                if len(drones) > 0:
                    drone = random.choice(drones)
                    return actions.FUNCTIONS.select_point("select_all_type", (drone.x, drone.y))

    def build_infestation_pit(self, obs):

        """
        Infestation Pit
        """
        lairs = self.get_units_by_type(obs, units.Zerg.Lair)
        if len(lairs) == 1:
            infestation_pits = self.get_units_by_type(obs, units.Zerg.InfestationPit)
            if len(infestation_pits) == 0:
                if self.unit_type_is_selected(obs, units.Zerg.Drone):
                    if self.can_do(obs, actions.FUNCTIONS.Build_InfestationPit_screen.id):
                        x = random.randint(0, 50)
                        y = random.randint(0, 50)

                        return actions.FUNCTIONS.Build_InfestationPit_screen("now", (x,y))

                drones = self.get_units_by_type(obs, units.Zerg.Drone)

                if len(drones) > 0:
                    drone = random.choice(drones)
                    return actions.FUNCTIONS.select_point("select_all_type", (drone.x, drone.y))

    def build_spire(self, obs):

        """
        Spire
        """
        lairs = self.get_units_by_type(obs, units.Zerg.Lair)
        if len(lairs) == 1:
            spire = self.get_units_by_type(obs, units.Zerg.Spire)
            if len(spire) == 0:
                if self.unit_type_is_selected(obs, units.Zerg.Drone):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Spire_screen.id):
                        x = random.randint(0, 50)
                        y = random.randint(0, 50)

                        return actions.FUNCTIONS.Build_Spire_screen("now", (x,y))

                drones = self.get_units_by_type(obs, units.Zerg.Drone)

                if len(drones) > 0:
                    drone = random.choice(drones)
                    return actions.FUNCTIONS.select_point("select_all_type", (drone.x, drone.y))

    def build_structure(self, obs, structure):

        """
        Spawning Pool
        """
        if structure == "spawning_pool":
            return self.build_spawning_pool(obs)

        """
        Roach Warren
        """
        if structure == "roach_warren":
            return self.build_roach_warren(obs)

        """
        Infestation Pit
        """
        if structure == "infestation_pit":
            return self.build_infestation_pit(obs)

        """
        Spire
        """
        if structure == "spire":
            return self.build_spire(obs)


    """
    Resources
    """

    def build_extractor(self, obs):
        """
        Build 2 Extractors
        """
        neutral_vespene_geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
        extractors = self.get_units_by_type(obs, units.Zerg.Extractor)

        if len(extractors) < 1 and len(neutral_vespene_geysers) > 0:
            if self.unit_type_is_selected(obs, units.Zerg.Drone):
                if self.can_do(obs, actions.FUNCTIONS.Build_Extractor_screen.id):
                    geyser = random.choice(neutral_vespene_geysers)
                    return actions.FUNCTIONS.Build_Extractor_screen("now", (geyser.x, geyser.y))

            drones = self.get_units_by_type(obs, units.Zerg.Drone)

            if len(drones) > 0:
                drone = random.choice(drones)
                return actions.FUNCTIONS.select_point("select_all_type", (drone.x, drone.y))

    def gather_vespene_gas(self,obs):

        """
        Gather Vespene Gas
        """
        extractor = self.get_units_by_type(obs, units.Zerg.Extractor)
        if len(extractor) > 0:
            extractor = random.choice(extractor)
            if extractor['assigned_harvesters'] < 3:
                if self.unit_type_is_selected(obs, units.Zerg.Drone):
                    if len(obs.observation.single_select) < 2 and len(obs.observation.multi_select) < 2 :
                        if self.can_do(obs,actions.FUNCTIONS.Harvest_Gather_screen.id):
                            return actions.FUNCTIONS.Harvest_Gather_screen("now",(extractor.x, extractor.y))


                drones = self.get_units_by_type(obs, units.Zerg.Drone)
                if len(drones) > 0 :
                    drone = random.choice(drones)
                    return actions.FUNCTIONS.select_point("select",(drone.x,drone.y))

    """
    Units
    """

    def morph_unit(self, obs, unit):
        if self.unit_type_is_selected(obs, units.Zerg.Larva):
            capacity = (obs.observation.player.food_cap - obs.observation.player.food_used)

            """
            Morph Overlord
            """
            if capacity < 2:
                if self.can_do(obs, actions.FUNCTIONS.Train_Overlord_quick.id):
                    return actions.FUNCTIONS.Train_Overlord_quick("now")

            """
            Morph Drone
            """
            if unit == "drone":
                if self.can_do(obs, actions.FUNCTIONS.Train_Drone_quick.id):
                    return actions.FUNCTIONS.Train_Drone_quick("now")

            """
            Morph Zergling
            """
            if unit == "zergling":
                if self.can_do(obs, actions.FUNCTIONS.Train_Zergling_quick.id):
                    return actions.FUNCTIONS.Train_Zergling_quick("now")

            """
            Morph Roach
            """
            if unit == "roach":
                if self.can_do(obs, actions.FUNCTIONS.Train_Roach_quick.id):
                    return actions.FUNCTIONS.Train_Roach_quick("now")

        """
        Select Larva
        """
        larvae = self.get_units_by_type(obs, units.Zerg.Larva)
        if len(larvae) > 0:
            larva = random.choice(larvae)
            return actions.FUNCTIONS.select_point("select_all_type", (larva.x, larva.y))

    def upgrade_structure(self, obs, structure):

        """
        Upgrade Hatchery -> Lair
        """
        if structure == "hatchery":
            lair = self.get_units_by_type(obs, units.Zerg.Lair)
            if len(lair) == 0:
                if self.unit_type_is_selected(obs, units.Zerg.Hatchery):
                    if self.can_do(obs, actions.FUNCTIONS.Morph_Lair_quick.id):
                        return actions.FUNCTIONS.Morph_Lair_quick("now")

                hatchery = self.get_units_by_type(obs, units.Zerg.Hatchery)
                if len(hatchery) > 0:
                    hatchery = random.choice(hatchery)
                    return actions.FUNCTIONS.select_point("select_all_type", (hatchery.x, hatchery.y))

        """
        Upgrade Lair -> Hive
        """
        if structure == "lair":
            hive = self.get_units_by_type(obs, units.Zerg.Hive)
            if len(hive) == 0:
                if self.unit_type_is_selected(obs, units.Zerg.Lair):
                    if self.can_do(obs, actions.FUNCTIONS.Morph_Hive_quick.id):
                        return actions.FUNCTIONS.Morph_Hive_quick("now")

                lair = self.get_units_by_type(obs, units.Zerg.Lair)
                if len(lair) > 0:
                    lair = random.choice(lair)
                    return actions.FUNCTIONS.select_point("select_all_type", (lair.x, lair.y))

    def step(self, obs):
        super(ZergAgent, self).step(obs)

        minerals = obs.observation.player.minerals


        """
        Attack Actions
        """

        if obs.first():
            player_y, player_x = (obs.observation.feature_minimap.player_relative == features.PlayerRelative.SELF).nonzero()

            xmean = player_x.mean()
            ymean = player_y.mean()

            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = [49,49]
                self.safe_coordinates = [12, 16]
            else:
                self.attack_coordinates = [12,16]
                self.safe_coordinates = [49,49]

        launch_sequence_1 = self.launch_attack(obs)
        if launch_sequence_1:
            return launch_sequence_1

        # Drones
        drones = self.get_units_by_type(obs, units.Zerg.Drone)
        if len(drones) < 8:
            drone = self.morph_unit(obs, "drone")
            if drone:
                return drone

        """
        Resources Actions
        """
        extractor = self.build_extractor(obs)
        if extractor:
            return extractor

        """
        Structures Actions
        """
        spawning_pool = self.build_structure(obs, "spawning_pool")
        if spawning_pool:
            return spawning_pool

        roach_warren = self.build_structure(obs, "roach_warren")
        if roach_warren:
            return roach_warren

        # Zerglings
        zerglings = self.get_units_by_type(obs, units.Zerg.Zergling)
        if len(zerglings) < 20:
            zergling = self.morph_unit(obs, "zergling")
            if zergling:
                return zergling

        # Roaches
        roaches = self.get_units_by_type(obs, units.Zerg.Roach)
        if len(roaches) < 5:
            roach = self.morph_unit(obs, "roach")
            if roach:
                return roach

        """
        Resource Gathering
        """
        gather_gas = self.gather_vespene_gas(obs)
        if gather_gas:
            return gather_gas

        """
        Evolution Actions
        """
        # upgrade_hatchery = self.upgrade_structure(obs, "hatchery")
        # if upgrade_hatchery:
        #     return upgrade_hatchery
        #
        # upgrade_lair = self.upgrade_structure(obs, "lair")
        # if upgrade_lair:
        #     return upgrade_lair

        # No action
        return actions.RAW_FUNCTIONS.no_op()

# Main Run Environment For Both Agents
def main(unused_argv):
    agent1 = ZergAgent()
    agent2 = TerranAgent()
    try:
        while True:
            with sc2_env.SC2Env(
                map_name="Simple64",
                players=[
                    sc2_env.Agent(sc2_env.Race.zerg),
                    sc2_env.Agent(sc2_env.Race.terran)
                    #sc2_env.Bot(sc2_env.Race.terran, sc2_env.Difficulty.easy)
                ],
                agent_interface_format=features.AgentInterfaceFormat(
                    feature_dimensions=features.Dimensions(screen=84, minimap=64),
                    use_feature_units=True
                ),
                step_mul=16,
                game_steps_per_episode=0,
                visualize=True
            ) as env:
                run_loop.run_loop([agent1,agent2], env)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    app.run(main)
