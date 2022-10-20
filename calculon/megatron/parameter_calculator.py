"""
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *  https://www.apache.org/licenses/LICENSE-2.0
 *
 * See the NOTICE file distributed with this work for additional information
 * regarding copyright ownership.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

import json

import calculon
from calculon.megatron import *

class ParameterCalculator(calculon.CommandLine):
  NAME = 'megatron-parameter-calculator'
  ALIASES = ['mpc']

  @staticmethod
  def create_parser(subparser):
    sp = subparser.add_parser(ParameterCalculator.NAME,
                              aliases=ParameterCalculator.ALIASES,
                              help='run a single megatron calculation')
    sp.set_defaults(func=ParameterCalculator.run_command)
    sp.add_argument('application', type=str,
                    help='File path to application configuration')
    sp.add_argument('-a', '--alignment', type=int, default=13,
                    help='Alignment spaces')

  @staticmethod
  def run_command(logger, args):
    with open(args.application, 'r') as fd:
      app_json = json.load(fd)

    try:
      app = Megatron.Application(app_json)
    except Megatron.Error as error:
      print(f'ERROR: {error}')
      return -1

    logger.info(f'{app.name}'
                f'{" " * (args.alignment - len(app.name))}'
                ' -> '
                f'{human_format(app.num_parameters())}')


calculon.CommandLine.register(ParameterCalculator)