import bisect


class RatedMoviesScheduling(object):
    def __init__(self, movies):
        
        # ordering our movies by finish time 
        self.movies = sorted(movies, key=lambda tup: tup[1])

        #initialinzg optimal solution as empty, used for memorization
        self.OPT = []
        self.solution = []


    def find_solution(self, j):
        '''
        Since we need to know which movies were selected
        here we have the post-processing responsible for doing that backtracking
        '''

        # base case
        if j == -1:
            return

        # find what movie was selected
        else:
            if (self.movies[j][2] + self.compute_opt(self.p[j])
                    ) > self.compute_opt(j - 1):
                self.solution.append(self.movies[j])
                self.find_solution(self.p[j])

            else:
                self.find_solution(j - 1)

    def previous_intervals(self):
        '''
        Responsible for deciding between orverlapping movies
        '''
        start = [movie[0] for movie in self.movies]
        finish = [movie[1] for movie in self.movies]
        p = []

        for i in range(len(self.movies)):
 
            # here we use bisect to find in which index we have to append the movie 
            # in order for the list to mantaint its ordination

            idx = bisect.bisect(finish, start[i]) - 1
            p.append(idx)

        return p

    def compute_opt(self, j):

        # base case
        if j == -1:
            return 0
        
        # that means we've already calculated OPT for that case, so we just use it
        elif (0 <= j) and (j < len(self.OPT)):
            return self.OPT[j]

        # calculating the optimal solution
        else:
            return max(self.movies[j][2] + self.compute_opt(self.p[j]),
                self.compute_opt(j -1))

    def weighted_interval(self):
        '''
        Calculates the optimal schedule
        Returns the resulting weight and the movies selected
        '''

        # base case
        if len(self.movies) == 0:
            return 0, self.solution

        # calculating everything for all movies
        self.p = self.previous_intervals()

        for j in range(len(self.movies)):
            opt_j = self.compute_opt(j)
            self.OPT.append(opt_j)

        self.find_solution(len(self.movies) - 1)
        
        # here we reverse the order of the solution because 
        # the backtracking returns the selected movies in reverse order
        return self.OPT[-1], self.solution[::-1]
