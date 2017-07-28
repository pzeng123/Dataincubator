## A Tower of Hanoi setup consists of N disks, weighing 1,…,N kilos. Each disk sits in one of M stacks, at positions 0,…,M−1. 
## All disks start stacked at position zero, ordered by weight with the lightest on top. At each point in time, a valid move can be made. 
## A valid move consists of taking the top disk off of one of the stacks and moving it to the top of the stack to the immediate left or right 
## (that is, at position one less or one greater than its current position), provided that the moved disk weighs less than all other disks at 
## its destination stack. For eample, in a N=M=3 problem with disks 1,2,3 at positions 0,1,2 respecitvely, the only valid moves are for 
## disk 1 to move to position 1 and disk 2 to move to position 2. We choose moves uniformly at random amongst all valid moves at a given time.
## We are interested in the position of the center of mass after T moves, that is ∑d×pd/∑d, where d is the disk weight and pd is the position
## of a disk weighing d.
##       ___________           ___________                   
##    0 | d1|   |   |       0 |   | d1|   |           
##      |___|___|___|         |___|___|___|         
##    1 | d2|   |   |       1 | d2|   |   |
##      |___|___|___|  =>     |___|___|___| 
##    2 | d3|   |   |       2 | d3|   |   |
##      |___|___|___|         |___|___|___| 
##        0   1   2             0   1   2
##            The first Move from state 0 to state 1. state number =    ∑ dn * N**(position of dn), represents the disks array
##
##      _________
##      | state1|----->  {next_state1:counts,    next_state2:counts, ...   }
##      |_______|
##      | state2|----->  {...}
##      |_______|
##      | ...   |...
##      |_______|
##      |       |
##      |_______|
##
##
##       Graph dictionary1,      Vertex dictionary2
##


## Center of Mass is 0.7777777778, Std is 0.3875638803 for M = N = 3, T = 16
## Center of Mass is 2.5004533463, Std is 0.7457665046 for M = N = 6, T = 256



import numpy as np


class Vertex(object):
    def __init__(self, node):
        self.id = node
        self.next = {}
        self.num_state = 0
        self.potential = 0
        self.potential_stored = 0
        
    def set_state(self, next_state):
        self.next[next_state] = 1
        self.num_state += 1
        
    def add_state_log(self, next_state, log=1):
        self.next[next_state] += log
    
    def get_id(self):
        return self.id

class Graph(object):
    def __init__(self):
        self.vert_dict = {}
        self.num_vert = 0
        
    def __iter__(self):
        return iter(self.vert_dict.values())
    
    def add_vertex(self, node):
        self.num_vert = self.num_vert + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex
        
    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
           return None
     
    def add_state(self, frm, next_state):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if next_state not in self.vert_dict:
            self.add_vertex(next_state)
        if next_state in self.vert_dict[frm].next:
            self.vert_dict[frm].add_state_log(next_state)
        else:
            self.vert_dict[frm].set_state(next_state)
        
    def get_all_vert(self):
        return self.vert_dict.keys()
             
def disks_to_num(array):
    '''convert the disk array to interger to save space
    
    '''
    num = 0
    stack_num = list(range(M))
    for row in range(N):
        temp = np.where(array[row,:] != 0)[0][0]
        num += N ** row * stack_num[temp]
    return num
 
def list_to_num(array_list):
    temp_list = array_list.copy()
    num = 0
    for i in range(len(temp_list)):
        num += temp_list[i] * N ** i
    return num
 
def num_to_disks(num):
    num_to_list = []
    for row in range(N):
        if num < N:
            num_to_list.append(num)
            for row_rest in range(row + 1, N):
                num_to_list.append(0)
            break
        else:
            num_to_list.append(num%N)
            num = num // N
    return num_to_list

## num_to_list and array_list [1 2 0] represents [top middle bottom]
def check_move(num, g):
    ''' Check move posibilities only if current state not recorded in graph.
    
    num is an integer, the initial state of this move
    g is an instence of Graph
    return moved_nums and g
    '''
    moved_nums = []
    array_list = num_to_disks(num)
    available_list = list(range(M))
    for index in range(N):
        disk_position = array_list[index]
        if disk_position in available_list:
            available_list.remove(disk_position)
            next_disk = array_list.copy()
            if array_list[index] + 1 in available_list:
                next_disk[index] =  array_list[index] + 1
                next_num = list_to_num(next_disk)
                moved_nums.append(next_num)
                g.add_state(num, next_num)
                       
            if array_list[index] - 1 in available_list:
                next_disk[index] =  array_list[index] - 1
                next_num = list_to_num(next_disk)
                moved_nums.append(next_num)
                g.add_state(num, next_num)
    return moved_nums, g
                
def next_move(num, g):
    ''' Disk move once.
    
    num is an integer, the initial state of this move
    g is an instence of Graph
    return next_num and g
    '''
    if num in g.vert_dict:
        if g.vert_dict[num].num_state != 0:
            current_vert = g.get_vertex(num)
            next_nums = []
            for next_state in current_vert.next:
                current_vert.add_state_log(next_state)
                g.vert_dict[next_state].potential += 1
            return next_nums, g
    next_nums, g = check_move(num, g)
    return next_nums, g

        
def main():
    Hanoi_array = np.zeros(shape = (N, M), dtype = int)
    Hanoi_array[:,0] = np.arange(1, N+1)
    nums = [disks_to_num(Hanoi_array)]
    g = Graph()
    center_of_mass = 0
    sd = 0 
    pre_move_status = 0
    move_status = 0
    
    for run_times in range(T):
        print('--------- No.{} moves --------'.format(run_times + 1))        
        state_vector = [0] * M**N
        
        
        ## use Vertex.potential to spread the connections in the future moves.
        for key_g in g.vert_dict:
            if g.vert_dict[key_g].potential != 0:
                for key_v in g.vert_dict[key_g].next:
                    g.vert_dict[key_v].potential_stored += 1
                    g.vert_dict[key_g].next[key_v] += 1                    
                g.vert_dict[key_g].potential -= 1
            else:
                g.vert_dict[key_g].potential = g.vert_dict[key_g].potential_stored
                g.vert_dict[key_g].potential_stored = 0
    
        cumul_nums = []
        for current_num in nums:
            temp_nums, g = next_move(current_num, g)
            cumul_nums.extend(temp_nums)
        nums = cumul_nums.copy()
      
        ## move_status - pre_move_status is the number of current move possibilities.
        for key_g in g.vert_dict:        
            for key_v in g.vert_dict[key_g].next:
                state_vector[key_v] += g.vert_dict[key_g].next[key_v]
                if run_times == T - 2:
                    pre_move_status += g.vert_dict[key_g].next[key_v]
                if run_times == T - 1:
                    move_status += g.vert_dict[key_g].next[key_v]
                
        # print graph
        # for (k,v) in g.vert_dict.items():
            # print('keys{} : next keys{}'.format(k,v.next))

        if run_times == T - 2:
            pre_state_vector = state_vector.copy()

    ## calculate center of mass mean and std
    cm_all = []    
    state_vector = np.subtract(state_vector, pre_state_vector)
    for index in range(len(state_vector)):
        num_to_list = num_to_disks(index)
        cm = [sum(np.multiply(num_to_list, np.arange(1,N+1)))/sum(range(N+1))] * state_vector[index]
        cm_all.extend(cm)
    mean_center_of_mass = center_of_mass / (move_status - pre_move_status)
    print('Center of Mass is {:.10f}, Std is {:.10f}'.format(np.mean(cm_all), np.std(cm_all)))

      
    
if __name__ == '__main__':

    M = 6
    N = 6
    T = 256
    
    main()




