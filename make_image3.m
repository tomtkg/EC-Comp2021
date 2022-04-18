function make_image3()
    load data.mat data %data = [naha42, naha256, hako42, hako256];
    for i = 2:2:8
        figure('Position',[100 100 480,360],'Visible','on');
        set(gca,'Fontname','Times New Roman','FontSize',13,'NextPlot','add', ...
            'Color','none','Box','on','LooseInset', get(gca, 'TightInset'));
        C = {'k-o','k:+','b-o','b:+','r-o','r:+'};
        minx = 100; miny = 100; maxx = 0; maxy = 0;
        if i < 5
            s = 18*(i-1); yint = 1; ystr =  'Objective value\it f';
        else
            s = 18*(i-5); yint = 0; ystr =  'Amount of payment';
        end
        for j = 1 : 6
            k = find(data(:,s+3*j-2));
            p(j) = plot(data(k,s+3*j-2), data(k,s+3*j-yint),C{j},'MarkerSize',3);
            minx = min(minx,min(data(k,s+3*j-2)));  miny = min(miny,min(data(k,s+3*j-yint)));
            maxx = max(maxx,max(data(k,s+3*j-2)));  maxy = max(maxy,max(data(k,s+3*j-yint)));
        end
        d = (maxx-minx)/30; xlim([minx-d maxx+d]);
        d = (maxy-miny)/30; ylim([miny-d maxy+d]);
        xlabel('Number of function evaluations');
        ylabel(ystr);
        label = [
            "Conventional formulation",...
            "Proposed formulation",...
            "\it b=\rm0, Consider \it f",...
            "\it b=\rm1, Consider \it f",...
            "\it b=\rm0, Consider \it f\rm and\it pay",...
            "\it b=\rm1, Consider \it f\rm and\it pay"];
        legend(p,label,'Color','white');
        exportgraphics(gcf,[num2str(i),'.eps'],'BackgroundColor','none','ContentType','vector');
        savefig([num2str(i),'.fig']);
        close;
    end
end
