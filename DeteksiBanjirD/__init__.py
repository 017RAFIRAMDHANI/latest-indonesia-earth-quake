"""
Aplikasi Gempa Terkini
MODULARISASI
"""
import requests
from bs4 import BeautifulSoup




class Bencana:
    def __init__(self,url,d):
        self.result = None
        self.url = url
        self.d = d

    def run(self):
        self.ekstraksi_data()
        self.tampilkan_data()
    def description(self):
        print(self.d)
class DeteksiBanjir(Bencana):
    def __init__(self,url):
        super(DeteksiBanjir, self).__init__(url,'s')


    def ekstraksi_data(self):
        try:
           content = requests.get(self.url)
        except Exception:
            return 'data gagal'
        if content.status_code == 200:

            soup = BeautifulSoup(content.text, 'html.parser')


            result = soup.find('span',{'class':'waktu'})
            result = result.text.split(', ')
            tanggal = result[0]
            waktu = result[1]



            result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')


            i =0
            magnitudo = None
            ls =None
            bt =None
            kedalaman =None

            pusat = None
            dirasakan = None
            lokasi = None

            for res in result:
                # print(i,res)
                if i == 1:
                    magnitudo = res.text
                elif i == 2:
                    kedalaman = res.text
                elif i == 3:
                    koordinat = res.text.split('- ')
                    ls = koordinat[0]
                    bt = koordinat[1]
                elif i == 4:
                    lokasi = res.text
                elif i == 5:
                    dirasakan = res.text
                i = i + 1

            hasil = dict()
            hasil['tanggal'] = tanggal
            hasil['waktu'] = waktu
            hasil['magnitudo'] = magnitudo
            hasil['kedalaman'] = kedalaman
            hasil['koordinat'] = {
                'ls' : ls, 'bt' : bt
            }
            hasil['lokasi'] = lokasi
            hasil['dirasakan'] = dirasakan

            self.result = hasil

        else:
            return None

    def tampilkan_data(self):
        if self.result is None:
            print('data gagal')
        print('Gempa Terakhir berdasarkan BMKG')
        print(f'Tanggal {self.result["tanggal"]}')
        print(f'Waktu {self.result["waktu"]}')
        print(f'Magnitudo {self.result["magnitudo"]}')
        print(f'Kedalaman {self.result["kedalaman"]}')
        print(f'Koordinat {self.result["koordinat"]["ls"]}, {self.result["koordinat"]["bt"]}')

        print(f'Lokasi {self.result["lokasi"]}')
        print(f'{self.result["dirasakan"]}')


class DeteksiGempa(Bencana):
    def __init__(self,url):
        super(DeteksiGempa, self).__init__(url,'m')
if __name__ == '__main__':
    bencana = DeteksiBanjir('https://bmkg.go.id')
    bencana.run()
    bencana.description()

    bencana = DeteksiGempa('NOT')
    bencana.description()




