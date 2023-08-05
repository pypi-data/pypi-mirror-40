import time
import numpy as np
import numpy
import kernelml

class ArgumentError(Exception):
    pass

### HDRE

def hdre_prior_sampler(kmldata):
    random_samples = kmldata.prior_random_samples
    num_params = kmldata.number_of_parameters-1
    lows,highs,_ = kmldata.args[-3:]
    parts = len(lows)
    sizes = np.linspace(0,num_params,(parts+1))[1:]/np.arange(0,parts+1)[1:]
    sizes[-1] = num_params-np.sum(sizes[:-1].astype(np.int))
    sizes[:-1] = sizes[:-1]
    sizes = sizes.astype(np.int)

    output = np.random.uniform(-1,1,size=(1,random_samples))
    i = 0
    j = 0
    while i<num_params:
        low = lows[j]
        high = highs[j]
        size = sizes[j]
        r = np.random.uniform(low=low,high=high,size=(size,random_samples))
        output = np.vstack([output,r])
        j+=1
        i+=num_params//parts
    return output



def hdre_parameter_transform(w,args):
    lows,highs,dim_map =  args[-3:]
    p = w[1:]
    count=0
    for low,high in zip(lows,highs):
        q = p[dim_map==count]
        q[q<low] = low
        q[q>high] = high
        p[dim_map==count]=q
        count+=1

    w[1:]=p
    return w

def hdre_histogram(data,bins=10):
    np=numpy
    vals,bins = np.histogramdd(data, normed=False,bins=bins)
    return vals,bins #,coords,mesh,

class HDRE():

    def __init__(self,num_clusters, bins_per_dim=13, simulations=500, realizations=20, smoothing_parameter=2.0,normalize=False):

        if (bins_per_dim/2 == bins_per_dim//2+1):
            raise ArgumentError("The number of bins per dimensions must be an odd integer")

        self.num_clusters = num_clusters
        self.simulations = simulations
        self.realizations = realizations
        self.smoothing_parameter = smoothing_parameter
        self.bins_per_dim = bins_per_dim
        self.normalize = normalize
        self.norm = 1

    def optimize(self,y,dview=None):

        def hdre_loss(x,y,w,args):
            np=numpy

            dim_combos,pdf_combos,bin_combos,fftkernel = args[:-3]

            var = np.abs(w[0])
            w = w[1:]
            num = y.shape[0]
            dim = y.shape[1]

            samples = 100
            inc = int(samples/(w.size/dim)+1)

            w = w.reshape((w.size//dim,dim))
            rv = np.zeros((samples,y.shape[1]))

            assert w.size//dim==w.size/dim

            n=y.shape[1]
            ll=0

            count=0
            for i,j in dim_combos:
                bins3 = [bin_combos[count,:,0],bin_combos[count,:,1]]
                lim = np.linspace(-var,var,100)
                _x_ = np.vstack([w[:,[i,j]]+x for x in lim])

                data1,_ = hdre_histogram(_x_,bins=bins3)
                data1=data1/np.sum(data1)
                pdf2 = pdf_combos[count]
                pdf1 = np.absolute(np.fft.ifftn(np.fft.fftn(data1)*fftkernel))

                diff = (pdf2-pdf1).flatten()*100

                ll += np.max(diff**2)
                count+=1


            return ll

        if self.normalize==True:
            self.norm = np.linalg.norm(y,axis=0)

        y = y/self.norm

        dim_combos = [(i,j) for i in range(y.shape[1]) for j in range(y.shape[1]) if j>i]
        half = (self.bins_per_dim)//2
        mesh = np.meshgrid(*[np.arange(-(half+1),half+2,1) for _ in range(2)])
        mesh = [d**2 for d in mesh]
        sigma = self.smoothing_parameter
        kernel = np.exp(-sum(mesh)/(2*sigma**2))/np.sqrt(2*np.pi*sigma**2)
        kernel = kernel/np.sum(kernel)
        fftkernel = np.fft.fftn(kernel)

        combo_len = len(dim_combos)
        pdf_combos = np.zeros((combo_len,self.bins_per_dim+2,self.bins_per_dim+2))
        bin_combos = np.zeros((combo_len,self.bins_per_dim+3,2))
        count=0
        for i,j in dim_combos:
            _y_ = y[:,[i,j]]
            bins=self.bins_per_dim
            data3, bins3 = hdre_histogram(_y_,bins=bins)
            bins3 = [np.concatenate([[-np.inf],_bins_,[np.inf]]) for _bins_ in bins3]
            bin_combos[count] = np.column_stack(bins3)
            data,_ = hdre_histogram(_y_,bins=bins3)
            data=data/np.sum(data)
            pdf_combos[count] = np.absolute(np.fft.ifftn(np.fft.fftn(data)*fftkernel))
            count+=1


        cycles = 100

        #The number of total simulations per realization = number of cycles * numer of simulations

        zcore = 2.0
        volume = 10
        volatility = 1
        zscore = 1

        self.num_dim = y.shape[1]

        param_to_dim = np.arange(0,self.num_dim*self.num_clusters)%self.num_dim

        args = [dim_combos,pdf_combos,bin_combos,fftkernel,np.min(y,axis=0),np.max(y,axis=0),param_to_dim]

        kml = kernelml.KernelML(
             prior_sampler_fcn=hdre_prior_sampler,
             posterior_sampler_fcn=None,
             intermediate_sampler_fcn=None,
             mini_batch_sampler_fcn=None,
             parameter_transform_fcn=hdre_parameter_transform,
             batch_size=None)

        if dview is not None:
             kml.use_ipyparallel(dview)

        kml.optimize(np.array([[]]),y[:1],loss_function=hdre_loss,
                                        convergence_z_score=3.0,
                                        min_loss_per_change=0.0,
                                        number_of_parameters=self.num_clusters*self.num_dim+1,
                                        args=args,
                                        number_of_realizations=self.realizations,
                                        number_of_random_simulations=self.simulations,
                                        update_volume=volume,
                                        update_volatility=volatility,
                                        number_of_cycles=cycles,
                                        plot_feedback=False,
                                        print_feedback=True)

        self.kmldata = kml.kmldata

    @property
    def variance_(self):
        w = self.kmldata.best_weight_vector.flatten()
        return np.abs(w[0])

    @property
    def centroids_(self):
        w = self.kmldata.best_weight_vector.flatten()
        w = w[1:]
        return w.reshape((w.size//self.num_dim,self.num_dim))

    def predict(self,y,variance_pad=1):

        var = self.variance_
        w = self.centroids_

        loss_matrix=np.zeros((y.shape[0],self.num_clusters))
        mask=np.zeros((y.shape[0],self.num_clusters))
        for i in range(w.shape[0]):
            m = (y/self.norm>w[i]+variance_pad*var)|(y/self.norm<w[i]-variance_pad*var)
            mask[:,i] = np.sum(m,axis=1)>0
            loss_matrix[:,i]=np.max(np.abs(y[:]-w[i]),axis=1)
        hdr_assignments=np.argmin(loss_matrix,axis=1).astype(np.float)
        hdr_assignments[np.sum(mask,axis=1)==self.num_clusters]=np.nan
        return hdr_assignments


