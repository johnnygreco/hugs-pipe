"""
Run hugs-pipe on an HSC patch.
"""

import os
import hugs_pipe

def main(tract, patch, config, outdir):
    data_id = {'tract': tract, 'patch': patch, 'filter': 'HSC-I'}
    hugs_pipe.utils.mkdir_if_needed(outdir)
    prefix = os.path.join(outdir, 'hugs-pipe-{}-{}'.format(tract, patch))
    if type(config)==str:
        config = hugs_pipe.Config(data_id=data_id, 
                                  config_fn=config, 
                                  log_fn=prefix+'.log')
    else:
        config.set_data_id(data_id)
    sources = hugs_pipe.run(config)
    sources.write(prefix+'.cat', format='ascii')

if __name__=='__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser('run hugs-pipe')
    parser.add_argument('-t', '--tract', type=int, help='HSC tract')
    parser.add_argument('-p', '--patch', type=str, help='HSC patch')
    parser.add_argument('-pl', '--patch_list', type=str, help='patch list', 
                        default=None)
    parser.add_argument('-c', '--config', type=str, help='config file name', 
                        default=None)
    parser.add_argument('-o', '--outdir', type=str, help='output directory', 
                        default='/home/jgreco/hugs-pipe-out')
    args = parser.parse_args()
    if args.patch_list is None:
        main(args.tract, args.patch, args.config, args.outdir)
    else:
        from astropy.table import Table
        log_fn = os.path.join(args.outdir, 'hugs-pipe.log')
        config = hugs_pipe.Config(log_fn=log_fn)
        regions = Table.read(args.patch_list, format='ascii')
        for tract, patch in regions['tract', 'patch']:
            main(tract, patch, config, args.outdir)
