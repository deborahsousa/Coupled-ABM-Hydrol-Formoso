/**
* Name: FRBModel 
* Authors: Déborah S. Sousa, Cássio G. C. Coelho, Conceição de M. A. Alves, Célia G. Ralha.
* Tags: irrigation; water regulation
*/
model UrubuRiverModel

global {
	//INPUTS
	//Files: matrices and shapefiles
	file shapefile_pumps <- file("../includes/urubu_pumps.shp"); //irrigation pumps from GAN
	matrix farmers_data <- file("../includes/urubu_farmers.csv"); //Farmer agents information
	list<string> daily_date <- file("../includes/daily.csv");
	matrix<float> prob_CI <- file("../includes/CI-prob.csv");
	matrix<float> prob_NC <- file("../includes/NC-prob.csv");
	matrix<float> prob_CP <- file("../includes/CP-prob.csv");
	matrix<float> limits_withdrawal <- file("../includes/limits-withdrawal.csv");
	/*file shapefile_hidro <- file("../includes/streamwork.shp"); //irrigation channels from SEMARH	
	file shapefile_channels <- file("../includes/irrigation_channels.shp"); //irrigation channels from SEMARH
	file shapefile_land <- file("../includes/area_urubu.shp"); // agricultural properties in the Urubu river basin
	geometry shape <- envelope(shapefile_land);*/
	
	//counters and time steps (dry season)
	date starting_date <- date("2020-04-30");
	float step <- 1 #day;
	int nb_days <- 123; //day count from the first to the last day of one dry season simulation
	string crop_season <- "soybean" among: ["soybean","rice"];
	//string day_of_the_year update: daily_date[cycle-1] init:'30/abr'; 
	int twoweeks_count update:update_twoweeks_count(cycle);
	
	//Biennium Plan rules
	float yellow_level <- 398; // centimeters
	float red_level <- 220; // centimeters
	date attention_date <- date("2020-07-01");
	date restriction_date <- date("2020-08-01");
	bool aux_date_08 update:(current_date >= restriction_date);
	bool aux_date_07 update:(current_date >= attention_date);	
	
	//list<float> f_daily_withdrawal update: Farmer collect sum (each.owned_pumps collect each.daily_withdrawal); //TODO
	list<float> all_pumps_daily_withdrawal update: Pump collect (each.daily_withdrawal);
	
	int day_in_twoweeks  update: update_day_in_twoweeks();

	action update_day_in_twoweeks type: int {
		if mod(cycle-1,15) != 0 or (cycle-1) >= 120 {
			return day_in_twoweeks + 1;
		} else {
			return 0;
		} 
	}
	
	action update_twoweeks_count (int cycle) type: int {
		if cycle = 0{
			return 0;
		}else if ((cycle-1) < 120) {
			return floor((cycle-1)/15);
		}else if ((cycle-1) >= 120) {
			return 7;
		}
	}
			
	//Scenarios
	//string scenario <- "S0"; //baseline
	//string scenario <- "S1" ;//all CP
	//string scenario <- "S2"; //all NC	
	string scenario <- "S3"; //all CI	
		
	//initial state
	init {
		//loading parameters for scenarios simulation
		/*create Land from: shapefile_land;
		create Channel from: shapefile_channels;
		create Hidro from: shapefile_hidro;*/
		
		//creating the Regulator agent
		create Regulator;
		
		//creating the Pump agent
		create Pump from: shapefile_pumps;
		list<int> farmer_id_list <- Pump collect each.f_id;
		list<int> farmer_id_list <- remove_duplicates(Pump collect each.f_id);
		list<int> pump_id_list <- Pump collect each.p_id;
		
		//creating the Farmer agent
		create Farmer number: length(farmer_id_list);
		int i <- 0;
		loop farmer over: Farmer {
			farmer.farmer_id <- farmer_id_list[i];
			i <- i + 1;
		}

		//relate farmers to profiles, demand group and area
		loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
			loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
				int my_farmer_data_id <- int(farmers_data[0,i]);
				if Farmer[j].farmer_id = my_farmer_data_id{
					Farmer[j].irrigation_area <- farmers_data[5,i]; 
					Farmer[j].demand_g <- farmers_data[3,i];
					Farmer[j].nb_pumps <- length(Farmer[j].owned_pumps); // number of owned pumps	
				}
			}
		}	
		
		//SCENARIOS	
		switch scenario {
			match 'S0'{
				loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
					loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
						int my_farmer_data_id <- int(farmers_data[0,i]);
						if Farmer[j].farmer_id = my_farmer_data_id{
							Farmer[j].profile <- farmers_data[2,i];
						}
					}
				}
			}
		
			match 'S1'{
				loop farmer over:Farmer {
					farmer.profile <- 'CP';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CP';
				} 
			}
			
			match 'S2'{
				loop farmer over:Farmer {
					farmer.profile <- 'NC';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'NC';
				} 
			}
			
			match 'S3'{
				loop farmer over:Farmer {
					farmer.profile <- 'CI';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CI';
				} 
			}			
		}	
		
		//relate pumps' owners profiles to their probabilities matrixes
		loop pump over:Pump {
			if pump.f_profile = 'CP'{
				pump.prob_matrix <- prob_CP;
			}else if pump.f_profile = 'NC'{
				pump.prob_matrix <- prob_NC;
			}else if pump.f_profile = 'CI'{
				pump.prob_matrix <- prob_CI;
			}
		} 
		
		//relate pumps to farmers 
		loop i from: 0 to: length(pump_id_list) - 1 step: 1 {
			loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
				if Pump[i].f_id = Farmer[j].farmer_id {
					add Pump[i] to: Farmer[j].owned_pumps;
					Pump[i].pump_owner <- Farmer[j];
					Pump[i].irrigation_area <- Farmer[j].irrigation_area;
				}
			}
		}
	}/******END INIT*****/		
			
	reflex save_daily_data when: cycle > 1 {		
		string day_of_the_year <- daily_date[cycle-1];
		save [cycle,int(self),day_of_the_year,all_pumps_daily_withdrawal] to: "../results/scenarios-reflexive/daily_withdrawal"+scenario+".csv"  type:csv rewrite:false header:false;				 
		//write 'ciclo '+cycle+' '+day_of_the_year+' '+' '+all_pumps_daily_withdrawal;
		//list<float> all_pumps_daily_withdrawal <- Pump collect (each.daily_withdrawal);	
		//save [cycle,int(self),day_of_the_year,all_pumps_daily_withdrawal]to: "../results/exemplo1.csv"  type:csv rewrite:false header:false;				
		//save [cycle,int(self),day_of_the_year,f_daily_withdrawal]to: "../results/daily_withdrawal-farmer-100.csv"  type:csv rewrite:false;
		//save [cycle,int(self),day_of_the_year,all_pumps_daily_withdrawal]to: "../results/daily_withdrawal-pumps-1000-keepseed"+scenario+"-init0.csv"  type:csv rewrite:false;
	}
	
	reflex end_simulation when:cycle=nb_days+2{
		do pause;
	}
}/******END GLOBAL*****/

species Pump {
	Pump pump;
	int p_id; //pump identification number
	string rotulo; // pump identification. Source: GAN (2022).
	int f_id; //farmer owner identification number
	matrix prob_matrix;
	list<float> p_list;
	Farmer pump_owner; //pump owner/farmer agent identification number
	string f_profile; //behaviour group of the pump's owner (cooperative profile)
	string demand_g; //demand group of the pump's owner. Source: Volken (2022).
	float irrigation_area; 
	int size <- 150;
	rgb color <- #black;
	float daily_withdrawal update:update_withdrawal(cycle);

	aspect default {
		draw circle(size) color: color border: #black;
	}
	
	action update_withdrawal (int cycle){
		list<float> p_list <- column_at(prob_matrix,twoweeks_count);
		int interval_index <- rnd_choice(p_list);
		float a <- limits_withdrawal[0,interval_index];
		float b <- limits_withdrawal[1,interval_index];
		return rnd(a,b);
	}
}

species Farmer {
	Farmer farmer;
	int farmer_id;
	string profile;
	string demand_g;
	list<Pump> owned_pumps; // list of owned pumps 
	int nb_pumps;
	float irrigation_area; //potential irrigation area [ha]
	float f_daily_withdrawal update: update_f_withdrawal();
	rgb color <- #grey;
	
	aspect default {
		draw circle(150) color: color border: #black;
	}

	action update_f_withdrawal {
		return sum(collect(owned_pumps,each.daily_withdrawal));
	}

	reflex assign_rules_reactions {
		bool is_respecting_red_rules <- false;
		bool is_respecting_yellow_rules <- false;
		
		if ((aux_date_08))= true {
			if f_daily_withdrawal = 0.0 {
				is_respecting_red_rules <- true;
			}
		}
		
		if(!is_respecting_red_rules){
			loop pump over: owned_pumps {
				pump.color <- #red;
				pump.size <- 200;
			}
		}else{
			loop pump over: owned_pumps {
				pump.color <- #black;
				pump.size <- 150;
			}
		}
	}
}

species Regulator{
	
}


// Auxiliar species for GUI experiments
species Land {

	aspect default {
		draw shape color: #darkgreen border: #black;
	}
}

species Channel {

	aspect default {
		draw shape color: #black border: #black;
	}
}

species Hidro {

	aspect default {
		draw shape color: #blue border: #black;
	}
}	

experiment teste_gui type: gui {
	output {
		display map refresh: every(1 #cycle) {
			species Hidro;
			species Channel;
			species Land;
			species Pump;
			species Farmer;
		}

		display Irrigation_per_pump refresh: every(1 #cycle) {
			chart "Individual water consumption (m³)" type: series {
				datalist Pump collect (each.rotulo) value: Pump collect (each.daily_withdrawal) style: line ;
			}
		}

		display Irrigation_per_farmer refresh: every(1 #cycle) {
			chart "Total water consumption (m³)" type: series {
				datalist Farmer collect string(each.farmer_id) value: Farmer collect sum (each.owned_pumps collect each.daily_withdrawal) style: line;
			}
		}
		
		display Irrigation_total refresh: every(1 #cycle) {
			chart "Total water consumption (m³)" type: series {
				data "All pumps" value: sum((Pump collect (each.daily_withdrawal))) style: line color: #black;
			}
		}

		display Irrigation_total_pump_profile refresh: every(1 #cycle) {
			chart "Water consumption (m³) per profile" type: series {
				data "CP" value: sum((Pump where (each.f_profile = "CP")) collect (each.daily_withdrawal)) style: line color: #magenta;
				data "CI" value: sum((Pump where (each.f_profile = "CI")) collect (each.daily_withdrawal)) style: line color: #cyan;
				data "NC" value: sum((Pump where (each.f_profile = "NC")) collect (each.daily_withdrawal)) style: line color: #yellow;
			}
		}
		
		display Irrigation_total_pump_group refresh: every(1 #cycle) {
			chart "Water consumption (m³) per profile" type: series {
				data "D1" value: sum((Pump where (each.demand_g = "D1")) collect (each.daily_withdrawal)) style: line color: #magenta;
				data "D2" value: sum((Pump where (each.demand_g = "D2")) collect (each.daily_withdrawal)) style: line color: #cyan;
				data "D3" value: sum((Pump where (each.demand_g = "D3")) collect (each.daily_withdrawal)) style: line color: #yellow;
			}
		}
		
		/*display AverageIrrigation_total_pump_profile refresh: every(1 #cycle) {
			chart "Average water consumption (m³) per pump per profile" type: series {
				data "CP" value: sum((Pump where (each.f_profile = "CP")) collect (each.daily_withdrawal))*length(Pump)/length(Pump where(each.f_profile = "CP")) color: #magenta;
				data "CI" value: sum((Pump where (each.f_profile = "CI")) collect (each.daily_withdrawal))*length(Pump)/length(Pump where(each.f_profile = "CI"))  color: #cyan;
				data "NC" value: sum((Pump where (each.f_profile = "NC")) collect (each.daily_withdrawal))*length(Pump)/length(Pump where(each.f_profile = "NC"))  color: #yellow;
			}
		}*/
	}
}

experiment repetitions type: batch repeat: 1000 autorun: true keep_seed:true until: cycle = nb_days+2 { 	
	reflex end_of_runs {
		int sim <- 0;
		ask simulations { // at the end of the simulation, for each simulation
			sim <- sim + 1;	
		}
	}
}