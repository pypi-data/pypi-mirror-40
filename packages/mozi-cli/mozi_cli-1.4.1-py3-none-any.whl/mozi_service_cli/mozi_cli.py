__author__ = 'Abdulrahman Semrie<hsamireh@gmail.com>'

import argparse
import os
import base64
import json
import click


class TargetParamType(click.ParamType):
    name = "target"

    def convert(self, value, param, ctx):
        if str.isalpha(value):
            return value
        else:
           raise click.BadParameter("{0} is not a valid column name".format(value))

@click.command()
@click.option("-j", default=8, type=click.IntRange(1, 15, clamp=True), help=""" Number of jobs allocated for deme 
                                        optimization.""")
@click.option("-m", default=10000, type=click.IntRange(1, None, clamp=True), help="Maximum number of fitness function evaluations.")
@click.option("--result-count", default=100, help="""The number of results to return, 
                                                    ordered according to a linear 
                                                    combination of score and complexity. If
                                                     negative, then return all results.""")
@click.option("--reduct-knob-building-effort", default=1, type=click.IntRange(0, 3),
              help="""Effort allocated for reduction during 
                        knob building, 0-3, 0 means minimum 
                        effort, 3 means maximum effort. The 
                        bigger the effort the lower the 
                        dimension of the deme""")
@click.option("--complexity-ratio", default=0.3, help="""Fix the ratio of the score to 
                                                complexity, to be used as a penalty, 
                                                when ranking the metapopulation for 
                                                fitness.
""")
@click.option("--enable-fs", default="1", type=click.Choice(["0", "1"]), help="""Enable integrated feature selection. 
    Feature selection is performed immediately before knob building (representation building), when creating a new deme.
                            """)
@click.option("--fs-algo", default="simple", type=click.Choice(["simple", "inc", "smd", "random", "hc"]),
              help="""Feature selection algorithm. Supported algorithms are:
                       simple: for a fast maximun mutual information algo.
                       inc: for incremental max-relevency, min-redundancy.
                       smd: for stochastic mutual dependency.
                       random: for uniform random dependency
                       hc: for moses-hillclimbing.""")
@click.option("--fs-target-size", default=20, help="""Feature count.  This option specifies the number of features to 
be selected out of the dataset.  A value of 0 disables feature selection.""")

@click.option("--balance", default="1", type=click.Choice(["0", "1"]), help="""If the table has discrete output type (
like bool or enum), balance the resulting ctable so all classes have the same weight.""")

@click.option("--hc-widen-Search", default="1", type=click.Choice(["0", "1"]), help="""Hillclimbing parameter (hc). If 
false,then deme search terminates when a local hilltop is found. If true, then the search radius is progressively 
widened, until another termination condition is met.""")
@click.option("--hc-crossover-pop-size", default=1000, help="""Number of new candidates created by crossover during 
each iteration of hillclimbing.""")
@click.option("--hc-crossover-min-neighbors", default=5000, help="""It also allows to control when 
                                        crossover occurs instead of exhaustive 
                                        search. If the neighborhood to explore 
                                        has more than the given number (and at 
                                        least 2 iterations has passed) then 
                                        crossover kicks in.""")
@click.argument("dataset", type=click.Path(exists=True, readable=True))
@click.argument("out", type=click.Path(exists=True, writable=True))
def cli(j, m, result_count, reduct_knob_building_effort, complexity_ratio, enable_fs, fs_algo, fs_target_size,
        balance, hc_widen_search, hc_crossover_pop_size, hc_crossover_min_neighbors,
        dataset, out):
    """
    :param dataset: The dataset file
    :param out: The dir to save the query.json file
    :return:
    """
    moses_opts_dict = {
        "-j": j, "--result-count": result_count, "--reduct-knob-building-effort": reduct_knob_building_effort,
        "-m": m, "--complexity-ratio": complexity_ratio, "--enable-fs": enable_fs,
        "--fs-algo": fs_algo, "--fs-target-size": fs_target_size, "--balance": balance,
        "--hc-widen-search": hc_widen_search,
        "--hc-crossover-pop-size": hc_crossover_pop_size,
        "--hc-crossover-min-neighbors": hc_crossover_min_neighbors
    }

    moses_opts_str = "".join("{} {} ".format(key, val) for key, val in moses_opts_dict.items())

    output_dict = {"mosesOpts": moses_opts_str + " -W 1"}

    # Prompt cross-val options

    folds = click.prompt("Num of folds: ", default=3)
    test_size = click.prompt("Test size: ", default=0.33, type=click.FloatRange(0, 1))
    seeds = click.prompt("Num of seeds: ", default=2)
    target = click.prompt("Name of the target feature", type=TargetParamType())

    cross_val_opts = {"folds": folds, "testSize": test_size, "randomSeed": seeds}

    output_dict["crossValOpts"] = cross_val_opts
    output_dict["target_feature"] = target

    output_dict["file@b64encode@dataset"] = dataset

    file = os.path.join(out, "query.json")
    with open(file, "w") as fp:
        fp.write(json.dumps(output_dict))

    click.echo(click.style("Done!", fg="green"))