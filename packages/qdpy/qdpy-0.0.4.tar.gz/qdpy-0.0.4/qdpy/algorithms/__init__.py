#    This file is part of qdpy.
#
#    qdpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    qdpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with qdpy. If not, see <http://www.gnu.org/licenses/>.

"""TODO"""


from qdpy.collections import *
import deap.tools
import numpy as np

from timeit import default_timer as timer
import pickle
import copy



def qdSimple(init_batch, toolbox, container, batch_size, niter, stats = None, halloffame = None, verbose = False, start_time = None, batch_callback = None):
    """The simplest QD algorithm using DEAP.
    :param init_batch: Sequence of individuals used as initial batch.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution operators.
    :param batch_size: The number of individuals in a batch.
    :param niter: The number of iterations.
    :param stats: A :class:`~deap.tools.Statistics` object that is updated inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :param start_time: Starting time of the illumination process, or None to take the current time.
    :param batch_callback: Optional callback funtion called when a new batch is generated. The callback function parameters are (iteration, batch, container, logbook).
    :returns: The final batch
    :returns: A class:`~deap.tools.Logbook` with the statistics of the
              evolution

    TODO
    """
    if start_time == None:
        start_time = timer()
    logbook = deap.tools.Logbook()
    logbook.header = ["iteration", "containerSize", "evals"] + (stats.fields if stats else []) + ["elapsed"]

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in init_batch if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit[0]
        ind.features = fit[1]

    # Update halloffame
    if halloffame is not None:
        halloffame.update(init_batch)

    # Store batch in container
    container.update(init_batch)

    # Compile stats and update logs
    record = stats.compile(container) if stats else {}
    logbook.record(iteration=0, containerSize=container.size_str(), evals=len(invalid_ind), elapsed=timer()-start_time, **record)
    if verbose:
        print(logbook.stream)
    # Call callback function
    if batch_callback != None:
        batch_callback(0, init_batch, container, logbook)

    # Begin the generational process
    for i in range(1, niter + 1):
        start_time = timer()
        # Select the next batch individuals
        batch = toolbox.select(container, batch_size)

        # Vary the pool of individuals
        offspring = []
        for o in batch:
            newO = toolbox.clone(o)
            ind, = toolbox.mutate(newO)
            del ind.fitness.values
            offspring.append(ind)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit[0]
            ind.features = fit[1]

        # Replace the current population by the offspring
        container.update(offspring)

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(container)

        # Append the current generation statistics to the logbook
        record = stats.compile(container) if stats else {}
        logbook.record(iteration=i, containerSize=container.size_str(), evals=len(invalid_ind), elapsed=timer()-start_time, **record)
        if verbose:
            print(logbook.stream)
        # Call callback function
        if batch_callback != None:
            batch_callback(i, batch, container, logbook)

    return batch, logbook


class ParallelismManager(object):
    """TODO"""
    def __init__(self, toolbox, parallelism_type = "multiprocessing"):
        self.orig_toolbox = toolbox
        self.toolbox = copy.deepcopy(toolbox)
        self.parallelism_type = parallelism_type

    def __enter__(self):
        """TODO"""
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """TODO"""
        self.close()

    def open(self):
        """TODO"""
        if self.parallelism_type == "none":
            self.map = map
        elif self.parallelism_type == "multiprocessing":
            import multiprocessing
            self.pool = multiprocessing.Pool()
            self.map = self.pool.map
        elif self.parallelism_type == "scoop":
            import scoop
            self.map = scoop.futures.map
        else:
            raise ValueError("Unknown parallelism_type: '%s'" % self.parallelism_type)
        self.toolbox.register("map", self.map)
        return self.toolbox

    def close(self):
        """TODO"""
        if self.parallelism_type == "none":
            pass
        elif self.parallelism_type == "multiprocessing":
            self.pool.close()
        elif self.parallelism_type == "scoop":
            pass
        else:
            raise ValueError("Unknown parallelism_type: '%s'" % self.parallelism_type)




class QDAlgorithm(object):
    """TODO"""

    def __init__(self, toolbox, container = None, stats = None, halloffame = None, iteration_filename = "iteration-%i.p", final_filename = "final.p", ea_fn = qdSimple, verbose = False, results_infos = None, save_period = None, **kwargs):
        self._update_params(**kwargs)
        self.toolbox = toolbox
        self.halloffame = halloffame
        self.iteration_filename = iteration_filename
        self.final_filename = final_filename
        self.ea_fn = ea_fn
        self.verbose = verbose
        self.save_period = save_period
        self._init_container(container)
        self._init_stats(stats)
        self._results_infos = {}
        if results_infos != None:
            self.add_results_infos(results_infos)


    def _init_container(self, container = None):
        """TODO"""
        if container == None:
            self.container = Container()
        else:
            self.container = container


    def _init_stats(self, stats = None):
        """TODO"""
        if stats == None:
            # Default stats
            self.stats = deap.tools.Statistics(lambda ind: ind.fitness.values)
            self.stats.register("avg", np.mean, axis=0)
            self.stats.register("std", np.std, axis=0)
            self.stats.register("min", np.min, axis=0)
            self.stats.register("max", np.max, axis=0)
        else:
            self.stats = stats


    def gen_init_batch(self, init_batch_size = None):
        """TODO"""
        if not hasattr(self, "start_time") or self.start_time == None:
            self.start_time = timer()
        if init_batch_size != None:
            self.init_batch_size = init_batch_size
        if not hasattr(self, "init_batch_size") or self.init_batch_size == None:
            raise ValueError("Please specify 'init_batch_size'")
        self.init_batch = self.toolbox.population(n = self.init_batch_size)


    def _update_params(self, **kwargs):
        """TODO"""
        for k,v in kwargs.items():
            if v != None:
                if k == "init_batch_size" or k == "batch_size" or k == "niter" or k == "start_time" or k == "save_period" or k == "iteration_filename" or k == "final_filename":
                    setattr(self, k, v)


    def _batch_callback(self, iteration, batch, container, logbook):
        """TODO"""
        self.current_iteration = iteration
        self.current_batch = batch
        if self.save_period == None or self.save_period == 0:
            return
        if iteration % self.save_period == 0 and iteration != self.niter and self.iteration_filename != None and self.iteration_filename != "":
            self.save(self.iteration_filename % self.current_iteration)


    def run(self, init_batch = None, **kwargs):
        """TODO"""
        self._update_params(**kwargs)
        # If needed, generate the initial batch
        if init_batch == None:
            if not hasattr(self, "init_batch") or self.init_batch == None:
                self.gen_init_batch()
        else:
            self.init_batch = init_batch
        # Run the illumination process !
        batch, logbook = self.ea_fn(self.init_batch, self.toolbox, self.container, self.batch_size, self.niter, stats = self.stats, halloffame = self.halloffame, verbose = self.verbose, start_time = self.start_time, batch_callback = self._batch_callback)
        if self.final_filename != None and self.final_filename != "":
            self.save(self.final_filename)


    def data_archive(self):
        """TODO"""
        results = {}
        def copy_attr(obj, names):
            for name in names:
                if hasattr(obj, name):
                    results[name] = getattr(obj, name)
        copy_attr(self, ['init_batch_size', 'batch_size', 'niter', 'container', 'current_iteration', 'current_batch', 'logbook', 'container'])
        #copy_attr(self.container, ['features_domain', 'fitness_domain', 'solutions', 'fitness', 'features', 'best_fitness', 'best_fitness_array'])
        results = {**results, **self._results_infos}
        return results


    def save(self, outputFile):
        """TODO"""
        results = self.data_archive()
        with open(outputFile, "wb") as f:
            pickle.dump(results, f)


    def add_results_infos(self, *args):
        """TODO"""
        if len(args) == 1:
            self._results_infos = {**self._results_infos, **args[0]}
        elif len(args) == 2:
            self._results_infos[args[0]] = args[1]
        else:
            raise ValueError("Please either pass a dictionary or key, value as parameter.")


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
