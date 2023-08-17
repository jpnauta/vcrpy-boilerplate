from simulations import BaseSimulator, SimulationFactory


class GoogleSimulator(BaseSimulator):
    def simulate_home_page(self, factory: SimulationFactory):
        # When this simulation is run:
        # - If re-playing cassettes, it will load `cassettes/google/home_page.yaml`
        # - If recording cassettes, it will record any requests in `cassettes/google/home_page.yaml`
        factory.use_cassette("google/home_page")

    def simulate_search(self, factory: SimulationFactory):
        # Multiple simulations can be defined for each simulator
        factory.use_cassette("google/search")
