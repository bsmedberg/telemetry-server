"""
Get the distribution of one or more boolean/enumerated measurements.
"""

import json

experimentid = "fx-dom.ipc.plugins.unloadTimeoutSecs-beta32@experiments.mozilla.org"

keys = [
    ("PLUGIN_STARTUP_MS", 20), # boolean
    ("NEWTAB_PAGE_SITE_CLICKED", 20), # 9-bucket
]

extra_histogram_entries = 6 # bucketN, sum, log_sum, log_sum_squares, sum_squares_lo, sum_squares_hi

def map(k, d, v, cx):
    if v.find(experimentid) == -1:
        return

    j = json.loads(v)
    info = j.get("info", {})
    active = info.get("activeExperiment", None)
    if active != experimentid:
        return
    activeBranch = info.get("activeExperimentBranch", None)

    histograms = j.get("histograms", {})

    for key, buckets in keys:
        if key in histograms:
            val = histograms[key]
            if len(val) != buckets + extra_histogram_entries:
                raise ValueError("Unexpected length for key %s: %s" % (key, val))
            for bucket in xrange(0, buckets):
                cx.write((activeBranch, key, bucket), val[bucket])

def reduce(k, v, cx):
    cx.writecsv(list(k) + [sum(v)])
