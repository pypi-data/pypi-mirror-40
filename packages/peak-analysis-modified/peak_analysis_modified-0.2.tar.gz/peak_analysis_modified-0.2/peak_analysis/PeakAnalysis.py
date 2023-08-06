class Peak:
    
    def __init__(self, centroid, sigma):
        self.centroid = float(centroid)
        self.sigma = float(sigma)
        self.spectrum_x = []
        self.spectrum_y = []
    
    def plot_spectrum(self):
        plt.plot(self.spectrum_x, self.spectrum_y)
        plt.xlabel('Channel')
        plt.ylabel('Count')
        plt.title('Spectrum')
        plt.show()
        
        
    def find_peak(self):
        '''
        Find the peak closest to the given centroid and update the centroid

        '''
        
        start = int(self.centroid)
        base_count = self.spectrum_y[start]
        if self.spectrum_y[start+1] > base_count:
            i = start
            while self.spectrum_y[i] <= self.spectrum_y[i+1]:
                i += 1
        else:
            i = start
            while self.spectrum_y[i] <= self.spectrum_y[i-1]:
                i -= 1
        self.centroid = i
        return self.centroid

    def read_data(self, filename):
        with open(filename) as file:
            x = []
            y = []

            for line in file:
            	x.append(float(line.strip().split(' ')[0]))
            	y.append(float(line.strip().split(' ')[1]))
            file.close()

            self.spectrum_x = x
            self.spectrum_y = y
            
    
    def get_area(self):
        left_bound = self.centroid - 3 * self.sigma
        right_bound = self.centroid + 3 * self.sigma
        area = 0
        for i in range(len(self.spectrum_x)):
            if self.spectrum_x[i] >=left_bound and self.spectrum_x[i] <= right_bound:
                area += self.spectrum_y[i]
        print(area)
        return area

    def __repr__(self):
        area = self.get_area()
        return 'Peak centroid {:.2f}, Area under the peak {:.2f}'.format(self.centroid, area)
