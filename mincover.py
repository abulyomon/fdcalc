import fileinput
import itertools

def print_relation(relation):
	for side in relation:
			print(side[0] + '->' + side[1])

def expand_relation_rhs(relation):
	expanded_relation = []
	for fd in relation:
		lhs = fd[0]
		rhs = fd[1]
		for rhs_set in list(rhs):
			expanded_relation.append([lhs, rhs_set])
	return expanded_relation

def build_trans_dict(relation):
	trans_dict = {}
	for fd in relation:
		lhs = fd[0]
		rhs = fd[1]
		if len(lhs) > 1:
			continue
		if lhs in trans_dict.keys():
			if rhs in trans_dict[lhs]:
				break
			else:
				trans_dict[lhs].append(rhs)
		else:
			trans_dict[lhs] = [rhs]
	return trans_dict

def traverse_dict(check_fd_left, check_fd_right, trans_dict):
	#print "DEBUG: Trying " + check_fd_left + ' vs ' + check_fd_right
	if check_fd_left in trans_dict.keys():
		#print "DEBUG: Checking " + check_fd_left + ' -> ' + check_fd_right
		if check_fd_right in trans_dict[check_fd_left]:
			#print "DEBUG: Good"
			return True
		else:
			#print "DEBUG: May be good later, traversing"
			for check_fd_right_ in trans_dict[check_fd_left]:
				#print "DEBUG: Forking as " + check_fd_right_ + ' vs ' + check_fd_right
				if traverse_dict(check_fd_right_, check_fd_right, trans_dict):
					#print "DEBUG: Good too"
					return True
	else:
		#print "DEBUG: Not good, out"
		return False

def reduce_relation_lhs(relation, trans_dict):
	for fd in relation:
		lhs = fd[0]
		if len(lhs) < 2:
			continue

		#Forward Pass
		set_changed = True
		while set_changed:
			set_changed = False
			set_pointer = 0
			lhs_set = list(lhs)
			while set_pointer < len(lhs_set) - 1:
				check_fd_left = lhs_set[set_pointer]
				check_fd_right = lhs_set[set_pointer + 1]
				if traverse_dict(check_fd_left, check_fd_right, trans_dict):
					lhs = lhs.translate(None, check_fd_right)
					set_changed = True
				set_pointer += 1

		#Backward Pass
		set_changed = True
		while set_changed:
			set_changed = False
			set_pointer = 0
			lhs_set = list(lhs)
			lhs_set.reverse()
			while set_pointer < len(lhs_set) - 1:
				check_fd_left = lhs_set[set_pointer]
				check_fd_right = lhs_set[set_pointer + 1]
				if traverse_dict(check_fd_left, check_fd_right, trans_dict):
					lhs = lhs.translate(None, check_fd_right)
					set_changed = True
				set_pointer += 1
		#Save changes
		fd[0] = lhs
	return relation

def build_cover_dict(relation):
	cover_dict = {}

	#Basic coverage
	for fd in relation:
		lhs = fd[0]
		rhs = fd[1]
		#Long LHS???
		if lhs in cover_dict.keys():
			if rhs in cover_dict[lhs]:
				break
			else:
				cover_dict[lhs].append(rhs)
		else:
			cover_dict[lhs] = [rhs]

	#Expanded coverage
	for lhs in cover_dict.keys():
		n = 2
		basic_set = ''.join(cover_dict[lhs])
		while n <= len(basic_set):
			cover_dict[lhs].extend(map(''.join,itertools.permutations(basic_set, n)))
			n += 1
	return cover_dict

def check_redundant(lhs, rhs, max_cover):
	#print "DEBUG: In check_redundant(" + lhs + ',' + rhs + ')'
	for right in max_cover[lhs]:
		#print "DEBUG: checking lhs " + lhs + " and right " + right
		if right in max_cover.keys():
			if rhs in max_cover[right]:
				return True
			else:
				return check_redundant(right, rhs, max_cover)
		else:
			pass
			#print "DEBUG: no keys"
	return False

def minimize(reduced_relation, max_cover):

	minimized_relation = []

	for fd in reduced_relation:
		lhs = fd[0]
		rhs = fd[1]
		#print "DEBUG: Checking if " + lhs + ' -> ' + rhs + " is redundant"
		if check_redundant(lhs, rhs, max_cover):
			pass
		else:
			minimized_relation.append(fd)

	return minimized_relation

######################

R = []
expanded_R = []

for line in fileinput.input():
	fd = line.strip().replace(" ", "").split('->',1)
	R.append(fd)

print_relation(R)
#############
print("(1) Expanding RHS:")
expanded_R = expand_relation_rhs(R)
print_relation(expanded_R)

print("(2) Reducing LHS:")

transitivity_dictionary = build_trans_dict(expanded_R)

#print "DEBUG: Transitivity Dictionary"
#print transitivity_dictionary

reduced_relation = reduce_relation_lhs(expanded_R,transitivity_dictionary)
print_relation(reduced_relation)

print("(3) Removing redundants FDs:")
max_cover = build_cover_dict(reduced_relation)
#print "DEBUG: Transitivity Dictionary"
#print max_cover

minimal_cover = minimize(reduced_relation, max_cover)
print_relation(minimal_cover)