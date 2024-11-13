#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <random>
#include <string>
using namespace std;
class Channel {
public:
    int bandwidth;
    int Tp;
    bool busy = false;
    std::string current_station;
    int busy_delay = 0;
    int finish_delay = 0;

    Channel(int bandwidth, int Tp) : bandwidth(bandwidth), Tp(Tp) {}
};

class Station {
public:
    std::string ID;
    int frame_size;
    Channel* channel;
    double p;
    bool ready = true;
    int waiting_period = 0;
    int drop_period = 0;
    int k = 0;
    bool jamming = false;
    int count = 0;
    int interrupted = 0;
    int dropped = 0;
    bool sending = false;
    // Station(Station &station)
    Station(){}
    Station(const std::string& ID, int frame_size, Channel* channel, double p) 
        : ID(ID), frame_size(frame_size), channel(channel), p(p) {}

    void exponential_backoff() {
        if (k < 15) {
            k++;
            waiting_period = rand() % (1 << k);
        } else {
            k = 0;
            drop_period = 5;
            dropped++;
        }
    }

    bool p_persistence() {
        if (sending) return false;
        if (drop_period > 0) {
            drop_period--;
            return false;
        }
        if (waiting_period == 0 && !channel->busy) {
            return ((double) rand() / RAND_MAX) < p;
        }
        if (waiting_period > 0) {
            waiting_period--;
            return false;
        }
        exponential_backoff();
        return false;
    }

    void interrupt() {
        channel->busy_delay = 0;
        channel->current_station.clear();
        jamming = true;
        sending = false;
        exponential_backoff();
        interrupted++;
    }
};

void simulate(std::unordered_map<std::string, Station>& stations, Channel& channel, int time) {
    int time_slots = time * 1000;

    std::ofstream log(".vscode/log.txt");
    while (time_slots > 0) {
        bool jamming = false;
        for (auto& [_, station] : stations) {
            if (station.jamming) {
                jamming = true;
                log << "Jamming by " << station.ID << "\n";
                station.jamming = false;
                break;
            }
        }

        if (jamming) {
            time_slots--;
            continue;
        }

        if (!channel.busy) {
            if (channel.busy_delay > 0) channel.busy_delay--;
            if (channel.finish_delay > 0) channel.finish_delay--;

            if (channel.busy_delay == 0 && !channel.current_station.empty()) {
                channel.busy = true;
                log << "Busy bit enabled\n";
            }

            std::vector<Station*> ready;
            for (auto& [_, station] : stations) {
                if (station.p_persistence()) ready.push_back(&station);
            }

            if (channel.current_station.empty() && ready.size() == 1) {
                channel.busy_delay = channel.Tp;
                channel.finish_delay = ready[0]->frame_size / channel.bandwidth;
                channel.current_station = ready[0]->ID;
                ready[0]->sending = true;
                log << ready[0]->ID << " started sending\n";
            } else if (!ready.empty()) {
                if (!channel.current_station.empty()) {
                    log << channel.current_station << " interrupted.\n";
                    stations[channel.current_station].interrupt();
                }
                log << "Exponential backoffs performed by: ";
                for (auto* station : ready) {
                    station->exponential_backoff();
                    log << station->ID << " ";
                }
                log << "\n";
            } else {
                log << ".\n";
            }
        } else {
            if (channel.finish_delay > 0) channel.finish_delay--;

            if (channel.finish_delay == 0) {
                stations[channel.current_station].count++;
                stations[channel.current_station].sending = false;
                stations[channel.current_station].drop_period = 1;
                channel.current_station.clear();
                channel.busy = false;
                log << "Transmission successful. Busy bit disabled\n";
            } else {
                log << ".\n";
            }
        }

        time_slots--;
    }
}

int main() {
    Channel channel(1000, 5);
    double P = 0.33;
    std::unordered_map<std::string, Station> stations;
    stations["X"] = Station("X", 12000, &channel, P);
    stations["Y"] = Station("Y", 12000, &channel, P);
    stations["Z"] = Station("Z", 12000, &channel, P);
    stations["B"] = Station("B", 12000,&channel, P);

    std::vector<double> times;
    std::vector<double> avgs;

    for (int i = 1; i < 150; i++) {
        double time = i / 10.0;
        simulate(stations, channel, static_cast<int>(time));
        
        int avg = 0;
        for (const auto& [id, station] : stations) {
            avg += station.count;
        }
        
        times.push_back(time);
        avgs.push_back(static_cast<double>(avg) / (time * 3));
    }

    // for (size_t i = 0; i < times.size(); ++i) {
    //     // std::cout << "Time: " << times[i] << ", Average: " << avgs[i] << std::endl;
    // }
    for(auto it: stations) {
        std::cout<<"ID: "<<it.second.ID<< "; Success: "<<it.second.count
        << "; Interrupted: "<< it.second.interrupted<<"; Dropped: "<<it.second.dropped<<endl;
    }
    return 0;
}
