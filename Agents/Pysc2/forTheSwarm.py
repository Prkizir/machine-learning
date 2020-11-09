from pysc2.agents import base_agent
from pysc2.lib import actions, features, units
from pysc2.env import sc2_env, run_loop
from absl import app

import random, time

class TerranAgent(base_agent.BaseAgent):
    def step(self, obs):
        super(TerranAgent, self).step(obs)
        return actions.RAW_FUNCTIONS.no_op()

class ZergAgent(base_agent.BaseAgent):

    """
    Upgrade Flags
    """
    upgrade_roach = False

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
    Structures
    """
    def build_spawning_pool(self, obs):
        spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
        if len(spawning_pools) == 0:
            if self.unit_type_is_selected(obs, units.Zerg.Drone):
                if self.can_do(obs, actions.FUNCTIONS.Build_SpawningPool_screen.id):
                    x = random.randint(0, 30)
                    y = random.randint(0, 30)

                    return actions.FUNCTIONS.Build_SpawningPool_screen("now", (x, y))

            drones = self.get_units_by_type(obs, units.Zerg.Drone)

            if len(drones) > 0:
                drone = random.choice(drones)
                return actions.FUNCTIONS.select_point("select_all_type", (drone.x, drone.y))

    def build_roach_warren(self, obs):
        spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
        if len(spawning_pools) == 1:
            roach_warrens = self.get_units_by_type(obs, units.Zerg.RoachWarren)
            if len(roach_warrens) == 0:
                if self.unit_type_is_selected(obs, units.Zerg.Drone):
                    if self.can_do(obs, actions.FUNCTIONS.Build_RoachWarren_screen.id):
                        x = random.randint(0, 30)
                        y = random.randint(0, 30)

                        return actions.FUNCTIONS.Build_RoachWarren_screen("now", (x, y))

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
    Resources
    """

    def build_extractor(self, obs):
        """
        Build 2 Extractors per Screen
        """
        neutral_vespene_geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
        extractors = self.get_units_by_type(obs, units.Zerg.Extractor)

        if len(extractors) < 2 and len(neutral_vespene_geysers) > 0:
            if self.unit_type_is_selected(obs, units.Zerg.Drone):
                if self.can_do(obs, actions.FUNCTIONS.Build_Extractor_screen.id):
                    geyser = random.choice(neutral_vespene_geysers)
                    return actions.FUNCTIONS.Build_Extractor_screen("now", (geyser.x, geyser.y))

            drones = self.get_units_by_type(obs, units.Zerg.Drone)

            if len(drones) > 0:
                drone = random.choice(drones)
                return actions.FUNCTIONS.select_point("select_all_type", (drone.x, drone.y))

    def gather_vespene_gas(self,obs):
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

    def upgrade_unit(self, obs, unit):
        """
        Roach -> Ravager
        """
        if unit == "roach":
            roaches = self.get_units_by_type(obs, units.Zerg.Roach)
            roach = random.choice(roaches)
            if self.can_do(obs, actions.FUNCTIONS.Morph_Ravager_quick.id):
                return actions.FUNCTIONS.Morph_Ravager_quick("now")

    def step(self, obs):
        super(ZergAgent, self).step(obs)

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

        """
        Units
        """

        # Drones
        drones = self.get_units_by_type(obs, units.Zerg.Drone)
        if len(drones) < 16:
            drone = self.morph_unit(obs, "drone")
            if drone:
                return drone

        # Zerglings
        zerglings = self.get_units_by_type(obs, units.Zerg.Zergling)
        if len(zerglings) < 20:
            zergling = self.morph_unit(obs, "zergling")
            if zergling:
                return zergling

        # Roaches
        roaches = self.get_units_by_type(obs, units.Zerg.Roach)
        if len(roaches) < 10 and not self.upgrade_roach:
            roach = self.morph_unit(obs, "roach")
            if roach:
                return roach

        ravagers = self.get_units_by_type(obs, units.Zerg.Ravager)
        if len(roaches) > 0 and len(ravagers) < 10 and self.upgrade_roach:
            ravager = self.upgrade_unit(obs, "roach")
            if ravager:
                return ravager

        """
        Resource Gathering
        """
        gather_gas = self.gather_vespene_gas(obs)
        if gather_gas:
            return gather_gas

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
