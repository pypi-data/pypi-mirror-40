# MIT license
#
# Copyright (C) 2016 by XESS Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Convert a netlist into an equivalent SKiDL program.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import int
from future import standard_library
standard_library.install_aliases()

import re
from collections import defaultdict
from kinparse import parse_netlist


def netlist_to_skidl(netlist_src):

    tab = ' ' * 4

    def legalize(name):
        """Make a string into a legal python variable name."""
        return re.sub('[^a-zA-Z0-9_]', '_', name)

    def comp_key(comp):
        """Create an ID key from component's major characteristics."""
        lib = comp.libsource.lib.val
        part = comp.libsource.part.val
        # Do not include the value in the key otherwise every capacitor or
        # resistor value will get its own template.
        try:
            footprint = comp.footprint.val
            return legalize('_'.join([lib, part, footprint]))
        except AttributeError:
            # Component has no assigned footprint.
            return legalize('_'.join([lib, part]))

    def template_comp_to_skidl(template_comp):
        """Instantiate a component that will be used as a template."""
        ltab = tab

        # Instantiate component template.
        name = comp_key(template_comp)  # python variable name for template.
        lib = template_comp.libsource.lib.val
        part = template_comp.libsource.part.val
        try:
            footprint = template_comp.footprint.val
            template_comp_skidl = "{ltab}{name} = Part('{lib}', '{part}', footprint='{footprint}', dest=TEMPLATE)\n".format(
                **locals())
        except AttributeError:
            template_comp_skidl = "{ltab}{name} = Part('{lib}', '{part}', dest=TEMPLATE)\n".format(
                **locals())

        # Set attributes of template using the component fields.
        for fld in template_comp.fields:
            template_comp_skidl += "{ltab}setattr({name}, '{fld.name.val}', '{fld.text}')\n".format(
                **locals())

        return template_comp_skidl

    def comp_to_skidl(comp, template_comps):
        """Instantiate components using the component templates."""
        ltab = tab

        # Use the component key to get the template that matches this component.
        template_comp_name = comp_key(comp)
        template_comp = template_comps[template_comp_name]

        # Get the fields for the template.
        template_comp_fields = {
            fld.name.val: fld.text
            for fld in template_comp.fields
        }

        # Create a legal python variable for storing the instantiated component.
        ref = comp.ref.val
        legal_ref = legalize(ref)

        # Instantiate the component and its value (if any).
        try:
            comp_skidl = "{ltab}{legal_ref} = {template_comp_name}(ref='{ref}', value='{comp.value.val}')\n".format(
                **locals())
        except AttributeError:
            comp_skidl = "{ltab}{legal_ref} = {template_comp_name}(ref='{ref}')\n".format(
                **locals())

        # Set the fields of the instantiated component if they differ from the values in the template.
        for fld in comp.fields:
            if fld.text != template_comp_fields.get(fld.name.val, ''):
                comp_skidl += "{ltab}setattr({legal_ref}, '{fld.name.val}', '{fld.text}')\n".format(
                    **locals())

        return comp_skidl

    def net_to_skidl(net):
        """Instantiate the nets between components."""

        # Build a list of component pins attached to the net.
        pins = []
        for n in net.nodes:
            comp = legalize(n.ref.val)  # Name of Python variable storing component.
            pin_num = n.pin.val  # Pin number of component attached to net.
            pins.append("{comp}['{pin_num}']".format(**locals()))
        pins = ', '.join(pins)  # String the pins into an argument list.

        ltab = tab

        # Instantiate the net, connect the pins to it, and return it.
        return "{ltab}Net('{net.name.val}').connect({pins})\n".format(**locals())

    def _netlist_to_skidl(ntlst):
        """Convert a netlist into a skidl script."""

        # Sequence of operations:
        #   1. Create a template for each component having a given library, part name and footprint.
        #   2. Instantiate each component using its matching template. Also, set any attributes
        #      for the component that don't match those in the template.
        #   3. Instantiate the nets connecting the component pins.
        #   4. Call the script to instantiate the complete circuit.
        #   5. Generate the netlist for the circuit.

        ltab = tab

        section_div = '#' + '=' * 79
        section_comment = "\n\n{ltab}{section_div}\n{ltab}# {section_desc}\n{ltab}{section_div}\n\n"

        skidl = ''
        skidl += '# -*- coding: utf-8 -*-\n\n'
        skidl += 'from skidl import *\n\n\n'
        circuit_name = legalize(ntlst.design.source.val)
        skidl += 'def {circuit_name}():'.format(**locals())

        section_desc = 'Component templates.'
        skidl += section_comment.format(**locals())
        comp_templates = {comp_key(comp): comp for comp in ntlst.components}
        template_statements = sorted(
            [template_comp_to_skidl(c) for c in list(comp_templates.values())])
        skidl += '\n'.join(template_statements)

        section_desc = 'Component instantiations.'
        skidl += section_comment.format(**locals())
        comp_inst_statements = sorted(
            [comp_to_skidl(c, comp_templates) for c in ntlst.components])
        skidl += '\n'.join(comp_inst_statements)

        section_desc = 'Net interconnections between instantiated components.'
        skidl += section_comment.format(**locals())
        net_statements = sorted([net_to_skidl(n) for n in ntlst.nets])
        skidl += '\n'.join(net_statements)

        ltab = ''
        section_desc = 'Instantiate the circuit and generate the netlist.'
        skidl += section_comment.format(**locals())
        ltab = tab
        skidl += 'if __name__ == "__main__":\n'
        skidl += '{ltab}{circuit_name}()\n'.format(**locals())
        skidl += '{ltab}generate_netlist()\n'.format(**locals())

        return skidl

    return _netlist_to_skidl(parse_netlist(netlist_src))
