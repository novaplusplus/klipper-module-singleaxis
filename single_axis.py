import logging
import stepper

class SingleAxisKinematics:
	def __init__(self, toolhead, config):
		self.printer = config.get_printer()
		
		new_rail = stepper.PrinterRail(config.getsection("stepper_x"))
		new_rail.setup_itersolve("cartesian_stepper_alloc", b'x')
		self.rail = new_rail

		for s in self.get_steppers():
			s.set_trapq(toolhead.get_trapq())
			toolhead.register_step_generator(s.generate_steps)
		self.printer.register_event_handler("stepper_enable:motor_off", self._motor_off)
		
		max_velocity, max_accel = toolhead.get_max_velocity()
		self.limit = (1.0, -1.0)
		r = new_rail.get_range()
		self.axes_min = toolhead.Coord(r[0], None, None, e=0.0)
		self.axes_max = toolhead.Coord(r[1], None, None, e=0.0)
		

	def get_steppers(self):
		return self.rail.get_steppers()

	
	def calc_position(self, stepper_positions):
		return [ stepper_positions[self.rail.get_name()] ]


	def set_position(self, newpos, homing_axes):
		self.rail.set_position(newpos)
		if 0 in homing_axes:
			self.limit = self.rail.get_range()


	def home(self, homing_state):
		axis = homing_state.get_axes()[0]
		position_min, position_max = self.rail.get_range()
		hi = self.rail.get_homing_info()
		homepos = [None, None, None, None]
		homepos[axis] = hi.position_endstop
		forcepos = list(homepos)
		if hi.positive_dir:
			forcepos[axis] -= 1.5 * (hi.position_endstop - position_min)
		else:
			forcepos[axis] += 1.5 * (position_max - hi.position_endstop)
		homing_state.home_rails([ self.rail ], forcepos, homepos)


	def _motor_off(self, print_time):
		self.limit = (1.0, -1.0)


	def _check_endstops(self, move):
		end_pos = move.end_pos[0]
		if (move.axes_d[0] and (end_pos < self.limit[0] or end_pos > self.limit[1])):
			if self.limit[0] > self.limit[1]:
				raise move.move_error("Must home axis first")
			raise move.move_error()


	def check_move(self, move):
		end_pos = move.end_pos[0]
		if end_pos < self.limit[0] or end_pos > self.limit[1]:
			self._check_endstops(move)
		else:
			return	


	def get_status(self, eventtime):
		h = "x" if self.limit[0] < self.limit[1] else ""
		return {
			"homed_axes": h,
			"axis_minimum": self.axes_min,
			"axis_maximum": self.axes_max,		
		}



def load_kinematics(toolhead, config):
	return SingleAxisKinematics(toolhead, config)
