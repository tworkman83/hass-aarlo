
import fnmatch
import pickle
import pprint
import threading


class ArloStorage(object):

    def __init__( self,arlo,name,storage_dir ):
        self._arlo = arlo
        self.file  = storage_dir + '/' + name + '.pickle'
        self.db    = {}
        self.lock  = threading.Lock()
        self.load()

    def _ekey( self,key ):
        return key if not isinstance( key,list ) else '/'.join( key )

    def _keys_matching( self,key ):
        mkeys = []
        ekey = self._ekey( key )
        for mkey in self.db:
            if fnmatch.fnmatch(mkey,ekey):
                mkeys.append( mkey )
        return mkeys

    def load( self ):
        try:
            with self.lock:
                with open( self.file,'rb' ) as dump:
                    self.db = pickle.load( dump )
        except:
            self._arlo.warning( 'file not read' )

    def save( self ):
        with self.lock:
            try:
                with open( self.file,'wb' ) as dump:
                    pickle.dump( self.db,dump, )
            except:
                self._arlo.warning( 'file not written' )

    def file_name( self ):
        return self.file

    def get( self,key,default=None ):
        with self.lock:
            ekey = self._ekey( key )
            return self.db.get(ekey,default)

    def get_matching( self,key,default=None ):
        with self.lock:
            gets = []
            for mkey in self._keys_matching( key ):
                gets.append( (mkey,self.db.get(mkey,default)) )
            return gets

    def keys_matching( self,key ):
        with self.lock:
            return self._keys_matching( key )

    def set( self,key,value ):
        ekey = self._ekey(key)
        output = ( 'set:' + ekey + '=' + str(value) )
        self._arlo.debug( output[:80] )
        with self.lock:
            self.db[ ekey ] = value
            return value

    def unset( self,key ):
        with self.lock:
            del self.db[ self._ekey( key ) ]

    def clear():
        with self.lock:
            self.db = {}

    def dump( self ):
        with self.lock:
            pprint.pprint( self.db )
