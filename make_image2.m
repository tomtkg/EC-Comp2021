function make_image2()
    for filename = {'iter0','iter4'}
        load(filename+".mat",'data')
        figure('Position',[100 100 480,360],'Visible','on');
        set(gca,'Fontname','ＭＳ 明朝','FontSize',13,'NextPlot','add', ...
            'Color','none','Box','on','LooseInset', get(gca, 'TightInset'));
        
        mini = min(data,[],1); maxi = max(data,[],1);
        if filename == "iter4"
            maxi(2) = 0.563952678; maxi(4) = 0.006023664; %Check
        end
        d = (maxi-mini)/20;
        
        yyaxis left
        plot(data(:,1), data(:,2),'-o','MarkerSize',3);
        ylabel('目的関数値 f');
        ylim([mini(2)-d(2) maxi(2)+d(2)]);
        yline(data(11,2),':'); %Check
        
        yyaxis right
        plot(data(:,1), data(:,4),'-o','MarkerSize',3);
        ylabel('最適化対象 y');
        ylim([mini(4)-d(4) maxi(4)+d(4)]);
        yline(0,':');
        
        xlabel('0→1に変更した変数の次元 i');
        %axis square;
        savefig(filename+".fig"); close;
    end
end
