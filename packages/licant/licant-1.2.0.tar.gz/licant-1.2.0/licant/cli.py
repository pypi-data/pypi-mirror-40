#coding: utf-8

import licant.util
from licant.core import WrongAction

import sys
from optparse import OptionParser

import os


def cli_argv_parse(argv):
	parser = OptionParser()
	parser.add_option("-d", "--debug", action="store_true",
					  default=False, help="print full system commands")
	parser.add_option("-t", "--trace", action="store_true",
					  default=False, help="print trace information")
	parser.add_option("-j", "--threads", default=1,
					  help="amount of threads for executor")
	parser.add_option("-q", "--quite", action="store_true",
					  default=False, help="don`t print shell operations")

	parser.add_option("--printruntime", action="store_true", default=False)

	opts, args = parser.parse_args(argv)
	return opts, args


def execute_with_default_action(target):
	if not hasattr(target, "default_action"):
		licant.util.error("target {} hasn't default_action (actions: {})"
			.format(licant.util.yellow(target.tgt), licant.util.get_actions(target)))
	return target.invoke(target.default_action, critical=True)

def	__cliexecute(args, default, core):
	if len(args) == 0:
		if default is None:
			licant.util.error("default target isn't set")

		target = core.get(default)
		return execute_with_default_action(target)

	fnd = args[0]

	# Try look up fnd in targets
	if fnd in core.targets:
		target = core.get(fnd)

		if len(args) == 1:
			return execute_with_default_action(target)

		act = args[1]

		if not target.hasaction(act):
			licant.util.error("{} is not action of target {}".format(
				licant.util.yellow(act),
				licant.util.yellow(fnd)))

		return target.invoke(act, *args[2:], critical=True)

	# Try look up fnd in actions of default_target
	if default is not None:
		dtarget = core.get(default)
		if dtarget.hasaction(fnd):
			return dtarget.invoke(fnd, *args[1:], critical=True)

	# Can't look fnd. 
	licant.util.error("Can't find routine " + licant.util.yellow(fnd) +
		". Enough target or default target's action with same name.")
	

def cliexecute(default=None, colorwrap=False, argv=sys.argv[1:], core=licant.core.core):
	if colorwrap:
		print(licant.util.green("[start]"))

	opts, args = cli_argv_parse(argv)

	core.runtime["debug"] = opts.debug or opts.trace
	core.runtime["trace"] = opts.trace
	core.runtime["quite"] = opts.quite

	cpu_count = os.cpu_count()
	core.runtime["threads"] = cpu_count if opts.threads == 'j' else int(opts.threads)

	if opts.printruntime:
		print("PRINT RUNTIME:", core.runtime)

	__cliexecute(args, default=default, core=core)		
		
	if colorwrap:
		print(licant.util.yellow("[finish]"))
