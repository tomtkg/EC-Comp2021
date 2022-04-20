function make_image4()
    for filename = {'iter0','iter4'}
        load(filename+".mat",'data')
        figure('Position',[100 100 480,360],'Visible','on');
        set(gca,'Fontname','Times New Roman','FontSize',13,'NextPlot','add', ...
            'Color','none','Box','on','LooseInset', get(gca, 'TightInset'));
        
        mini = min(data,[],1); maxi = max(data,[],1);
        if filename == "iter4"
            maxi(2) = 0.563952678; maxi(4) = 0.006023664; %Check
        end
        d = (maxi-mini)/20;
        
        yyaxis left
        plot(data(:,1), data(:,2),'-o','MarkerSize',3);
        ylabel('Objective value\it f');
        ylim([mini(2)-d(2) maxi(2)+d(2)]);
        yline(data(11,2),':'); %Check
        
        yyaxis right
        plot(data(:,1), data(:,4),'-o','MarkerSize',3);
        ylabel('Optimization target\it y');
        ylim([mini(4)-d(4) maxi(4)+d(4)]);
        yline(0,':');
        
        xlabel('Dimension\it i\rm changed from 0 to 1');
        exportgraphics(gcf,filename+".eps",'BackgroundColor','none','ContentType','vector');
        savefig(filename+".fig"); close;
    end
end
