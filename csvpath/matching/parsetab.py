
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'match_partCLOSE_PAREN EQUALS HEADER_SYM LEFT_BRACKET NAME NUMBER OPEN_PAREN QUOTE REGEX RIGHT_BRACKET VAR_SYMmatch_part : LEFT_BRACKET expression RIGHT_BRACKET\n                      | LEFT_BRACKET expressions RIGHT_BRACKET\n        expressions : expression\n                       | expressions expression\n        expression : function\n                        | equality\n                        | header function : NAME OPEN_PAREN CLOSE_PAREN\n                    | NAME OPEN_PAREN equality CLOSE_PAREN\n                    | NAME OPEN_PAREN function CLOSE_PAREN\n        equality : function EQUALS term\n                    | function EQUALS var_or_header\n                    | var_or_header EQUALS function\n                    | var_or_header EQUALS term\n                    | var_or_header EQUALS var_or_header\n                    | term EQUALS var_or_header\n                    | term EQUALS function\n        term : QUOTE NAME QUOTE\n                | NUMBER\n                | REGEX\n        var_or_header : header\n                         | var\n        var : VAR_SYM NAME header : HEADER_SYM NAME\n                  | HEADER_SYM NUMBER\n        '
    
_lr_action_items = {'LEFT_BRACKET':([0,],[2,]),'$end':([1,17,18,],[0,-1,-2,]),'NAME':([2,3,4,5,6,7,11,12,13,14,15,16,19,21,22,23,24,25,27,28,29,30,31,34,35,36,37,38,39,40,41,],[8,-3,8,-5,-6,-7,24,-19,-22,26,-20,27,-4,8,8,8,-24,-25,-23,-11,-12,-21,-8,-16,-17,-15,-13,-14,-18,-9,-10,]),'HEADER_SYM':([2,3,4,5,6,7,12,13,15,19,20,21,22,23,24,25,27,28,29,30,31,34,35,36,37,38,39,40,41,],[11,-3,11,-5,-6,-7,-19,-22,-20,-4,11,11,11,11,-24,-25,-23,-11,-12,-21,-8,-16,-17,-15,-13,-14,-18,-9,-10,]),'QUOTE':([2,3,4,5,6,7,12,13,15,19,20,21,23,24,25,26,27,28,29,30,31,34,35,36,37,38,39,40,41,],[14,-3,14,-5,-6,-7,-19,-22,-20,-4,14,14,14,-24,-25,39,-23,-11,-12,-21,-8,-16,-17,-15,-13,-14,-18,-9,-10,]),'NUMBER':([2,3,4,5,6,7,11,12,13,15,19,20,21,23,24,25,27,28,29,30,31,34,35,36,37,38,39,40,41,],[12,-3,12,-5,-6,-7,25,-19,-22,-20,-4,12,12,12,-24,-25,-23,-11,-12,-21,-8,-16,-17,-15,-13,-14,-18,-9,-10,]),'REGEX':([2,3,4,5,6,7,12,13,15,19,20,21,23,24,25,27,28,29,30,31,34,35,36,37,38,39,40,41,],[15,-3,15,-5,-6,-7,-19,-22,-20,-4,15,15,15,-24,-25,-23,-11,-12,-21,-8,-16,-17,-15,-13,-14,-18,-9,-10,]),'VAR_SYM':([2,3,4,5,6,7,12,13,15,19,20,21,22,23,24,25,27,28,29,30,31,34,35,36,37,38,39,40,41,],[16,-3,16,-5,-6,-7,-19,-22,-20,-4,16,16,16,16,-24,-25,-23,-11,-12,-21,-8,-16,-17,-15,-13,-14,-18,-9,-10,]),'RIGHT_BRACKET':([3,4,5,6,7,12,13,15,19,24,25,27,28,29,30,31,34,35,36,37,38,39,40,41,],[17,18,-5,-6,-7,-19,-22,-20,-4,-24,-25,-23,-11,-12,-21,-8,-16,-17,-15,-13,-14,-18,-9,-10,]),'EQUALS':([5,7,9,10,12,13,15,24,25,27,30,31,33,39,40,41,],[20,-21,22,23,-19,-22,-20,-24,-25,-23,-21,-8,20,-18,-9,-10,]),'OPEN_PAREN':([8,],[21,]),'CLOSE_PAREN':([12,13,15,21,24,25,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,],[-19,-22,-20,31,-24,-25,-23,-11,-12,-21,-8,40,41,-16,-17,-15,-13,-14,-18,-9,-10,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'match_part':([0,],[1,]),'expression':([2,4,],[3,19,]),'expressions':([2,],[4,]),'function':([2,4,21,22,23,],[5,5,33,35,37,]),'equality':([2,4,21,],[6,6,32,]),'header':([2,4,20,21,22,23,],[7,7,30,30,30,30,]),'term':([2,4,20,21,23,],[9,9,28,9,38,]),'var_or_header':([2,4,20,21,22,23,],[10,10,29,10,34,36,]),'var':([2,4,20,21,22,23,],[13,13,13,13,13,13,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> match_part","S'",1,None,None,None),
  ('match_part -> LEFT_BRACKET expression RIGHT_BRACKET','match_part',3,'p_match_part','matcher.py',65),
  ('match_part -> LEFT_BRACKET expressions RIGHT_BRACKET','match_part',3,'p_match_part','matcher.py',66),
  ('expressions -> expression','expressions',1,'p_expressions','matcher.py',74),
  ('expressions -> expressions expression','expressions',2,'p_expressions','matcher.py',75),
  ('expression -> function','expression',1,'p_expression','matcher.py',83),
  ('expression -> equality','expression',1,'p_expression','matcher.py',84),
  ('expression -> header','expression',1,'p_expression','matcher.py',85),
  ('function -> NAME OPEN_PAREN CLOSE_PAREN','function',3,'p_function','matcher.py',96),
  ('function -> NAME OPEN_PAREN equality CLOSE_PAREN','function',4,'p_function','matcher.py',97),
  ('function -> NAME OPEN_PAREN function CLOSE_PAREN','function',4,'p_function','matcher.py',98),
  ('equality -> function EQUALS term','equality',3,'p_equality','matcher.py',112),
  ('equality -> function EQUALS var_or_header','equality',3,'p_equality','matcher.py',113),
  ('equality -> var_or_header EQUALS function','equality',3,'p_equality','matcher.py',114),
  ('equality -> var_or_header EQUALS term','equality',3,'p_equality','matcher.py',115),
  ('equality -> var_or_header EQUALS var_or_header','equality',3,'p_equality','matcher.py',116),
  ('equality -> term EQUALS var_or_header','equality',3,'p_equality','matcher.py',117),
  ('equality -> term EQUALS function','equality',3,'p_equality','matcher.py',118),
  ('term -> QUOTE NAME QUOTE','term',3,'p_term','matcher.py',134),
  ('term -> NUMBER','term',1,'p_term','matcher.py',135),
  ('term -> REGEX','term',1,'p_term','matcher.py',136),
  ('var_or_header -> header','var_or_header',1,'p_var_or_header','matcher.py',147),
  ('var_or_header -> var','var_or_header',1,'p_var_or_header','matcher.py',148),
  ('var -> VAR_SYM NAME','var',2,'p_var','matcher.py',156),
  ('header -> HEADER_SYM NAME','header',2,'p_header','matcher.py',162),
  ('header -> HEADER_SYM NUMBER','header',2,'p_header','matcher.py',163),
]
